from odoo import models, fields, api
from lxml import etree
import base64

import logging
_logger = logging.getLogger(__name__)

class Part(models.Model):
    _inherit = 'certificate_planer.part'


    def _has_certificate(self):
        self.ensure_one()
        return bool(self.certificate_id)


    def action_export_xml(self):
        return self._export_to_xml()

    def _export_to_xml(self):
        transactions_el = etree.Element("transactions")
        transaction_el = etree.SubElement(transactions_el, "transaction", date="12345") 
        document_el = etree.SubElement(transaction_el, "document") 
        _logger.warning(f"document_el: {document_el}")
        configuration_el = etree.SubElement(document_el, "configuration") 
        counter = 0
        for part in self:
            if part._has_certificate():
                attribute_el = etree.SubElement(configuration_el, "attribute", Certificate=part.certificate_id.part_id.name)
                counter += 1

        if counter > 0:
            xml_string = etree.tostring(
                transactions_el, pretty_print=True, encoding="UTF-8", xml_declaration=True
            )

            # --- Encode for Odoo ---
            xml_b64 = base64.b64encode(xml_string)

            # --- Create attachment ---
            attachment = self.env['ir.attachment'].create({
                'res_model': self._name,
                'res_id': self.id,
                'name': f'part_{self.id}.xml',
                'datas': xml_b64,
                'type': 'binary',
                'mimetype': 'application/xml',
            })

            # --- Trigger download ---
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }
        else:
            return False
        
