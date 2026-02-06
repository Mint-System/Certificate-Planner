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

        # confirmation of change status if new status is configured to trigger export
        if self.status_id.pdm_export_trigger:
            return {
                "type": "ir.actions.act_window",
                "res_model": "certificate_planer.change_status_confirm",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_change_id": self.change_id.id,
                    "new_status": self.status_id.id,
                },
            }

        # Change status without confirmation and export if new status is not configured to trigger export
        change = self.change_id
        new_status_id = self.status_id.id
        change.write({"status_id": new_status_id})

        return {
            "type": "ir.actions.act_window",
            "res_model": "certificate_planer.change",
            "res_id": self.change_id.id,
            "view_mode": "form",
        }
