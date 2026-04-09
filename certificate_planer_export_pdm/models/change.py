import os
import logging
from lxml import etree
import base64
import datetime

from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Change(models.Model):
    """
    Collect all parts belonging to the change and build a list a tree's from bottom (leaf nodes) to top parent part(s).
    Generate XML from the tree list and export it as file or attachment.
    """
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


    def _action_export_xml(self):
        self.ensure_one()

        xml_data = self._gen_xml() 

        export_type = self.env['ir.config_parameter'].sudo().get_param('certificate_planer_export_pdm.pdm_export_type')
        if export_type == 'attachment':
            return self._export_to_attachment(xml_data)
        else:
            return self._export_to_file(xml_data)

    def _gen_xml(self):
        """Called by _action_export_xml and _action_export_to_attachment.
        Export XML for this change, including all parts in the BOM structure.
        """
        self.ensure_one()

        _logger.warning(f"self: {self}")

        certificate = self.certificate_id
        _logger.warning(f"certificate: {certificate}")
        part = certificate.part_id
        _logger.warning(f"part: {part}")
        

        _logger.warning("Collect parts")
        tree_list = self._collect_parts(part)

        _logger.warning("Collect certificates and EMS")
        self.env['certificate_planer.part']._collect_certificates_ems(tree_list)
        # self._collect_certificates_ems(tree_list)

        # generate XML
        xml_str = self.env['certificate_planer.xml_export']._treelist_to_xml(tree_list)
        return xml_str

    def _get_file_name(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f'change_{self.id}_export_{timestamp}.xml'
        return fname

    def _export_to_attachment(self, xml_data):
        self.ensure_one()

        fname = self._get_file_name()

        xml_b64 = base64.b64encode(xml_data)

        attachment = self.env['ir.attachment'].create({
            'name': fname,
            'type': 'binary',
            'datas': xml_b64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/xml',
            'description': 'pdm export',
        })

        _logger.warning(f"attachment: {attachment}")

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def _export_to_file(self, xml_data):
        self.ensure_one()
        # xml_data = self._gen_xml()
        # _logger.warning(f"xml_data: {xml_data}")

        # define export directory and ensure it exists
        export_dir = '/mnt/addons/certificate_planer_export_pdm/exports'
        os.makedirs(export_dir, exist_ok=True)

        fname = self._get_file_name()

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