import os
import logging
from lxml import etree
import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Change(models.Model):
    _inherit = "certificate_planer.change"
    
    def _collect_parts(self, root_part):
        visited = root_part.walk_down()
        visited = root_part.walk_up(visited)
        return self.env['certificate_planer.part'].browse(list(visited))

    def _find_top_part(self, parts):
        """Return the part with no parents."""
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
        self.ensure_one()

        _logger.warning(f"self: {self}")

        certificate = self.certificate_id
        _logger.warning(f"certificate: {certificate}")
        part = certificate.part_id
        _logger.warning(f"part: {part}")

        parts = self._collect_parts(part)
        top = self._find_top_part(parts)

        _logger.warning(f"parts: {parts}")
        _logger.warning(f"top: {top}")
            
        top_certificate = top._get_certificate()
        _logger.warning(f"top certificate: {top_certificate}")

        # Top-level attribute if certificate exists
        if top and top_certificate:
            root = etree.Element("transactions")
            transaction_el = etree.SubElement(root, "transaction", date="12345") 
            document_el = etree.SubElement(transaction_el, "document") 
            attr = etree.SubElement(root, "attribute")
            attr.set("name", "Certificate")
            attr.text = top_certificate.part_id.name

            for part in parts:
                configuration_el = etree.SubElement(document_el, "configuration") 
                certificate = part._get_certificate().part_id.name if part._get_certificate() else ""
                attribute_el = etree.SubElement(configuration_el, "attribute", Certificate=certificate)

        return etree.tostring(
            root, 
            pretty_print=True, 
            xml_declaration=False, 
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