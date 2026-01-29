from odoo import fields, models

class ChangeExportConfirm(models.TransientModel):
    _name = "certificate_planer.change_export_confirm"
    _description = "Confirm XML Export"

    change_id = fields.Many2one("certificate_planer.change")

    def action_confirm_export(self):
        self.ensure_one()

        # as attachment
        self.change_id._action_export_to_attachment()

    
        # self.change_id._action_export_to_file()

        
        return {"type": "ir.actions.act_window_close"}
