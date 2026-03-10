import os
import logging
from lxml import etree
import base64
import datetime

from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Change(models.Model):
    _inherit = "certificate_planer.change"
    
    def _collect_parts(self, root_part):
        """Collect all parts in the BOM structure starting from root part (initiator of the change on top).
        """

        # construct tree from change (top) until children without children (leaf nodes)
        tree_root = root_part.tree_down()

        # children without children (leaf nodes)
        leaf_nodes = [node for node in tree_root.descendants if not node.children]
        child_part_list = [self.env['certificate_planer.part'].browse(leaf_node.part_id) for leaf_node in leaf_nodes]

        # upside down: from leaf nodes (children without children) up to their parents
        tree_list = []
        for part in child_part_list:
            tree = part.walk_up_bigtree()
            tree_list.append(tree)
        
        return tree_list

    def _collect_certificates_ems(self, tree_list):
        for tree in tree_list:
            root = tree
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

    def _action_export_to_attachment(self):
        self.ensure_one()

        xml_data = self._export_change_to_xml() 

        fname = f'change_{self.id}_approved.xml'
        xml_b64 = base64.b64encode(xml_data)

        attachment = self.env['ir.attachment'].create({
            'name': fname,
            'type': 'binary',
            'datas': xml_b64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/xml',
        })

        _logger.warning(f"attachment: {attachment}")

        return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }

    def _action_export_to_file(self):
        self.ensure_one()
        xml_data = self._export_change_to_xml()
        _logger.warning(f"xml_data: {xml_data}")

        # define export directory and ensure it exists
        export_dir = '/mnt/addons/certificate_planer_export_pdm/exports'
        os.makedirs(export_dir, exist_ok=True)

        # File name
        fname = f'change_{self.id}_export.xml'
        file_path = os.path.join(export_dir, fname)
        _logger.warning(f"export file path: {file_path}")

        # Write the file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_data.decode('utf-8'))

            _logger.info(f"Exported Change {self.id} to {file_path}")
            self.message_post(
                body=f"XML export created: {file_path}",
                subject="XML Export",
                message_type='notification'
            )
        except Exception as e:
            _logger.exception("Export failed")
            raise UserError(str(e))

        return True


    def _export_change_to_xml(self):
        """Called by _action_export_to_file and _action_export_to_attachment.
        Export XML for this change, including all parts in the BOM structure.
        """
        self.ensure_one()

        _logger.warning(f"self: {self}")

        certificate = self.certificate_id
        _logger.warning(f"certificate: {certificate}")
        part = certificate.part_id
        _logger.warning(f"part: {part}")
        

        _logger.warning("Start collect Parts")
        tree_list = self._collect_parts(part)
        _logger.warning("End collect Parts.")

        _logger.warning("Start Certificates collecte")
        self._collect_certificates_ems(tree_list)
        _logger.warning("End Certificates collected.")

        # generate XML
        xml_str = self.env['certificate_planer.xml_export']._treelist_to_xml(tree_list)
        return xml_str

    def _build_tree(self, root_parts):
        root_nodes = []
        for root_part in root_parts:
            root_node = Node(root_part.name)
            root_nodes.append(root_node)
            self._build_tree_helper(root_part, root_node)
        return root_nodes

    def _build_tree_helper(self, part, node):
        for bom_line in part.part_ids:
            child_part = bom_line.certificate_planer_part_id
            child_node = Node(child_part.name, parent=node)
            self._build_tree_helper(child_part, child_node)

    def _print_tree(self, tree):
        export_dir = '/tmp/odoo_exports'
        os.makedirs(export_dir, exist_ok=True)

        for tree_node in tree:
            fname = f'change_{self.id}_export_{tree_node.name}.png'
            file_path = os.path.join(export_dir, fname)
            UniqueDotExporter(tree_node).to_picture(file_path)