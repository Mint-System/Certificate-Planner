import base64
import datetime
import logging
import os

from bigtree import Node

from odoo import models

_logger = logging.getLogger(__name__)


class Part(models.Model):
    _inherit = "certificate_planer.part"

    def _has_certificate(self):
        self.ensure_one()
        return bool(self.certificate_id)

    def _get_certificate(self):
        """Return a singleton certificate for this part (or False)"""
        self.ensure_one()
        part = self
        # model
        certificate = self.env["certificate_planer.certificate"].search([("part_id", "=", part.id)], limit=1)
        return certificate or False

    def _collect_certificates_ems(self, tree_list):
        for tree in tree_list:
            root = tree

            # edge case: top part, no children (in case of export some selected parts)
            if root.is_leaf:
                root.collected_certificates = [root.certificate_id] if root.certificate_id else []
                root.collected_ems = [root.part_name] if root.is_ems_equipment else []
            else:
                for descendant in root.descendants:
                    # save certificate ids and ems for this node ...
                    this_certificate_id = descendant.certificate_id
                    this_is_ems_equipment = descendant.is_ems_equipment
                    this_part_name = descendant.part_name

                    if not hasattr(descendant, "collected_certificates"):
                        descendant.collected_certificates = []
                    if this_certificate_id:
                        descendant.collected_certificates.append(this_certificate_id)

                    if not hasattr(descendant, "collected_ems"):
                        descendant.collected_ems = []
                    if this_is_ems_equipment:
                        descendant.collected_ems.append(this_part_name)

                    # ... and all its ancestors
                    for ancestor in descendant.ancestors:
                        if not hasattr(ancestor, "collected_certificates"):
                            ancestor.collected_certificates = []
                        if this_certificate_id:
                            ancestor.collected_certificates.append(this_certificate_id)

                        if not hasattr(ancestor, "collected_ems"):
                            ancestor.collected_ems = []
                        if this_is_ems_equipment:
                            ancestor.collected_ems.append(this_part_name)

    def tree_down(self, tree_root=None, parent=None):
        """
        Recursively build a bigtree Node structure representing the BOM hierarchy.
        Walks from this part down to all child parts (top-to-bottom).
        """
        self.ensure_one()
        node_name = f"{self.name} ({self.designation})"
        node = Node(
            node_name,
            part_id=self.id,
            part_name=self.name,
        )
        if not parent:
            # root node
            tree_root = node
        else:
            node.parent = parent

        for part in self:
            for bom_line in part.part_ids:
                child = bom_line.certificate_planer_part_id
                if child:
                    child.tree_down(tree_root=tree_root, parent=node)

        return tree_root

    def walk_up_bigtree(self):
        """
        Build a bigtree Node structure representing the reverse BOM hierarchy.
        Walks from this part up to all parent assemblies (bottom-to-top).

        Returns:
            bigtree.Node: Root node representing this part, with children nodes
                          representing parent assemblies in the BOM hierarchy.
                          Returns None if bigtree is not installed.

        Example:
            part = self.env['certificate_planer.part'].search([('name', '=', 'F partnr')])
            tree = part.walk_up_bigtree()
            if tree:
                from bigtree import print_tree
                print_tree(tree, attr_list=["part_id", "level"])
        """
        self.ensure_one()

        # Create node for current part with all relevant attributes
        node_name = f"{self.name} ({self.designation})"
        node = Node(
            node_name,
            part_id=self.id,
            part_name=self.name,
            certificate_id=self.env["certificate_planer.certificate"].search([("part_id", "=", self.id)]),
            is_ems_equipment=self.is_ems_equipment,
        )

        self._walk_up_bigtree_recursive(node)

        return node

    def _walk_up_bigtree_recursive(self, parent_node):
        """
        Helper method for walk_up_bigtree to recursively build the tree.

        Args:
            parent_node: The bigtree Node to attach children to
            visited: Set of part IDs already visited (to prevent cycles)
            level: Current depth level in the tree
        """
        self.ensure_one()

        for bom in self.parent_bom_ids:
            parent_part = bom.part_id

            if parent_part:
                _logger.warning(f"parent_part: {parent_part.id}")
                node_name = f"{parent_part.name} ({parent_part.designation})"
                child_node = Node(
                    node_name,
                    parent=parent_node,
                    part_id=parent_part.id,
                    part_name=parent_part.name,
                    certificate_id=self.env["certificate_planer.certificate"].search(
                        [("part_id", "=", parent_part.id)]
                    ),
                    is_ems_equipment=parent_part.is_ems_equipment,
                )

                # Recursively process this parent's parents
                parent_part._walk_up_bigtree_recursive(child_node)

    def _action_export_all_xml(self):
        # self.ensure_one()

        xml_data = self._gen_xml()

        export_type = self.env["ir.config_parameter"].sudo().get_param("certificate_planer_export_pdm.pdm_export_type")
        if export_type == "attachment":
            return self._export_to_attachment(xml_data)
        else:
            # 'file'
            return self._export_to_file(xml_data)

    def _gen_xml(self):
        """
        Called by _action_export_xml and _action_export_to_attachment.
        Export XML for this change, including all parts in the BOM structure.
        self: Record set of all parts selected for export
        """
        # loop over all selected parts, build tree for each part and collect certificates and EMS info for all trees
        _logger.warning("Collect parts")
        for part in self:
            _logger.warning(f"Exporting part: {part.id} - {part.name}")
        tree_list = []
        for part in self:
            tree = part.walk_up_bigtree()
            tree_list.append(tree)
        _logger.warning(f"Built {len(tree_list)} trees for export.")

        # collect certificates and EMS info for all trees
        self._collect_certificates_ems(tree_list)

        # generate XML
        xml_str = self.env["certificate_planer.xml_export"]._treelist_to_xml(tree_list)
        return xml_str

    def _get_file_name(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"parts_export_{timestamp}.xml"
        return fname

    def _export_to_attachment(self, xml_data):
        fname = self._get_file_name()

        xml_b64 = base64.b64encode(xml_data)

        attachment = self.env["ir.attachment"].create(
            {
                "name": fname,
                "type": "binary",
                "datas": xml_b64,
                "mimetype": "application/xml",
                "description": "pdm export",
            }
        )

        _logger.warning(f"attachment: {attachment}")

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }

    def _export_to_file(self, xml_data):
        # define export directory and ensure it exists
        export_dir = "/mnt/addons/certificate_planer_export_pdm/exports"
        os.makedirs(export_dir, exist_ok=True)

        # File name
        fname = self._get_file_name()

        file_path = os.path.join(export_dir, fname)
        _logger.warning(f"export file path: {file_path}")

        # Write the file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(xml_data.decode("utf-8"))

            _logger.info(f"Exported {len(self)} Parts to {file_path}")
            # Optionale Benachrichtigung aber muss an einen Part gebunden sein
            # self[0].message_post(
            #     body=f"XML export created: {file_path}",
            #     subject="XML Export",
            #     message_type='notification'
            # )
        except Exception as e:
            _logger.exception(f"Export failed: {e}")
            raise UserError(str(e))

        return True
