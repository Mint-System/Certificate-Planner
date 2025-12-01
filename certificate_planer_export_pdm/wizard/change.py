from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ChangeWizard(models.TransientModel):
    _inherit = 'certificate_planer.change.wizard'


    def set_status(self):
        self.ensure_one()
        _logger.warning("CALLED")

        change = self.change_id
        new_status = self.status_id

        change.write({"status_id": new_status.id})

        # confirmation of export
        if new_status.pdm_export_trigger:
            return {
                "type": "ir.actions.act_window",
                "res_model": "certificate_planer.change_export_confirm",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_change_id": change.id,
                },
            }

        # No export required, return to form
        return {
            "type": "ir.actions.act_window",
            "res_model": "certificate_planer.change",
            "res_id": change.id,
            "view_mode": "form",
        }
