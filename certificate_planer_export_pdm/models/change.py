import os
import logging
from lxml import etree
import base64
import copy
import datetime

# from anytree import Node
# from anytree.exporter import UniqueDotExporter

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Change(models.Model):
    _inherit = "certificate_planer.change"
    
    def _collect_parts(self, root_part):
        """Collect all parts in the BOM structure starting from root part (initiator of the change).
        Called by _export_change_to_xml.
        """
        # find all children of the root part
        visited = root_part.walk_down()

        # find all parents of the visited parts
        visited_tmp = copy.copy(visited)

        # collect certs for this part from his parents
        path_lists_dict = {}
        for part in visited_tmp:
            path_lists_dict[part.id] = []
            visited = part.walk_up(path_lists_dict[part.id], visited)


        # tree = self._build_tree(root_parts)
        # self._print_tree(tree)
        
        # NOTE: meaning?
        return visited, path_lists_dict
        # return self.env['certificate_planer.part'].browse(list(visited))

    # NOTE: Old version, may be not needed anymore
    # def _collect_parts(self, root_part):
    #     """Collect all parts in the BOM structure starting from root_part.
    #     Called by _export_change_to_xml.
    #     """
    #     visited = root_part.walk_down()
    #     visited = root_part.walk_up(visited)
    #     return self.env['certificate_planer.part'].browse(list(visited))

    def _find_top_part(self, parts):
        """Return the part with no parents.
        called by _export_change_to_xml."""
        for part in parts:
            if not part.parent_bom_ids:
                return part
        return None

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

        export_dir = '/tmp/odoo_exports'
        os.makedirs(export_dir, exist_ok=True)

        # File name
        fname = f'change_{self.id}_export.xml'
        file_path = os.path.join(export_dir, fname)

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
        except:
            raise UserError(_('no export'))

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
        

        parts, path_lists_dict = self._collect_parts(part)
        # _logger.critical(f"collected parts: {parts}")
        for part in parts:
            _logger.critical(f"PDMEXP: part: {part.name}")
            # _logger.critical(f"PDMEXP: part: {part}, certificate: {part.certificate_id.id if part.certificate_id else 'None'}")
            # _logger.critical(f"part: {part}, certificate: {part._get_certificate()}")

        # for part in parts:            
        #     # part._get_certificate().part_id.name if part._get_certificate() else ""
        #     _logger.critical(f"part: {part}")
        #     # _logger.critical(f"part: {part}, certificate: {part.certificate_id.id if part.certificate_id else 'None'}")
        #     # _logger.critical(f"part: {part}, certificate: {part._get_certificate()}")

        # return etree.tostring(
        #     etree.Element(
        #         "test"
        #     ),
        #     pretty_print=True,
        #     xml_declaration=False,
        #     encoding="UTF-8",
        # )

        # TODO: does top part have a certificate?
        # top = self._find_top_part(parts)

        _logger.critical(f"PDMEXP: parts: {parts}")
        # _logger.warning(f"top: {top}")



        # top_certificate = top._get_certificate()
        # _logger.warning(f"top certificate: {top_certificate}")

        now_epoch = int(datetime.datetime.now().timestamp())
        # NOTE: Temporary simple XML for testing
        # Top-level attribute if certificate exists
        # if top and top_certificate:
        root = etree.Element("transactions")
        # transaction_el = etree.SubElement(root, "transaction", date=f"{now_epoch}", type="wf_import_document_attributes", vaultname="Aerolite") 
        # document_el = etree.SubElement(transaction_el, "document") 
        # conf_el = etree.SubElement(document_el, "configuration", name="Standard", quantity="1") 
        # attr = etree.SubElement(root, "attribute")
        # attr.set("name", "Certificate")
        # attr.text = top_certificate.part_id.name

        for part in parts:
            _logger.critical(f"PDMEXP: part: {part.name}, {part.id}")
            # try:
            #     certificate = part.certificate_id.id
            # except:
            #     certificate = None
            # certificate = part._get_certificate()
            # _logger.critical(f"part cert: {certificate}")
            if part.id in path_lists_dict:
                certificates_str = ";".join(f"{part_id}" for part_id in path_lists_dict[part.id])
                # certificates_str = ";".join(path_lists_dict[part.id])
            else:
                certificates_str = f"{part.id} hat nur ein Zertifikat"
            transaction_el = etree.SubElement(root, "transaction", date=f"{now_epoch}", type="wf_import_document_attributes", vaultname="Aerolite") 
            document_el = etree.SubElement(transaction_el, "document") 
            conf_el = etree.SubElement(document_el, "configuration", name="Standard", quantity="1") 
            # _logger.critical(f"part in XML export: {part.id}, {part.designation}, {part.certificate_id.id if part.certificate_id else 'None'}")
            attr_el = etree.SubElement(conf_el, "attribute", name="Artikelnummer", value=part.name)
            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=';'.join(cert_collection[part.id]) if part.id in cert_collection else "")
            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=certificate.display_name if certificate else "")
            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=f"{certificate}")
            attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=certificates_str)
            
            # <attribute name="Aircraft type" value="PC-24"/>
            attr_el = etree.SubElement(conf_el, "attribute", name="Aircraft type", value=part.designation)
            # part.certificate_id.aircraft_type_id.name if part.certificate_id else ""
            
            # configuration_el = etree.SubElement(document_el, "configuration") 
            # certificate = part._get_certificate().part_id.name if part._get_certificate() else ""
            # attribute_el = etree.SubElement(configuration_el, "attribute", Certificate=certificate)

        return etree.tostring(
            root, 
            pretty_print=True, 
            xml_declaration=True, 
            encoding="UTF-8"
        )

    # @api.model
    # def write(self, vals):
    #     _logger.warning(f"vals: {vals}")
    #     # Capture previous statuses before write
    #     previous_status = {rec.id: rec.status_id for rec in self}
    #     _logger.warning(f"previous_status: {previous_status}")

    #     res = super().write(vals)

    #     for rec in self:
    #         new_status = rec.status_id
    #         _logger.warning(f"new status: {new_status}")

    #         if 'status_id' in vals:
    #             old = previous_status.get(rec.id)
    #             _logger.warning(f"old: {old}")
    #             if not old or old != new_status:
    #                 if new_status and new_status.pdm_export_trigger:
    #                     rec._action_export_to_file()

    #     return res

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