from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class ChangeWizard(models.TransientModel):
    _inherit = 'certificate_planer.change.wizard'

    change_status_text = fields.Char(string="Test Text")

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['change_status_text'] = self.env['ir.config_parameter'].sudo().get_param('certificate_planer_export_pdm.change_status_text')
        return res

    def set_status(self):
        self.ensure_one()

        _logger.warning("CALLED")

        self.change_status_text = self.env['ir.config_parameter'].sudo().get_param('certificate_planer_export_pdm.change_status_text')

        change = self.change_id
        new_status = self.status_id

        # trigger export if status requires it
        change.write({"status_id": new_status.id})

        # No export required, return to form
        return {
            "type": "ir.actions.act_window",
            "res_model": "certificate_planer.change",
            "res_id": change.id,
            "view_mode": "form",
        }
