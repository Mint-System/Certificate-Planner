from odoo import api, fields, models

class ChangeExportConfirm(models.TransientModel):
    _name = "certificate_planer.change_export_confirm"
    _description = "Confirm XML Export"

    change_id = fields.Many2one("certificate_planer.change")

    def action_confirm_export(self):
        self.ensure_one()
        self.change_id._action_export_to_file()

        
        return {"type": "ir.actions.act_window_close"}
