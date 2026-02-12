from odoo import fields, models

class ChangeStatusConfirm(models.TransientModel):
    _name = "certificate_planer.change_status_confirm"
    _description = "Confirm Status Change"

    change_id = fields.Many2one("certificate_planer.change")
    change_status_confirm_text = fields.Char(string="Test Text")

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['change_status_confirm_text'] = self.env['ir.config_parameter'].sudo().get_param('certificate_planer_export_pdm.change_status_confirm_text')
        return res

    def action_confirm_status(self):
        """
        change status to new status and export XML
        """

        self.ensure_one()

        change = self.change_id
        new_status_id = self.env.context.get("new_status")

        change.write({"status_id": new_status_id})

        export_type = self.env['ir.config_parameter'].sudo().get_param('certificate_planer_export_pdm.pdm_export_type')
        if export_type == 'attachment':
            # as attachment
            self.change_id._action_export_to_attachment()
        else:
            # export as XML file
            self.change_id._action_export_to_file()

        
        return {"type": "ir.actions.act_window_close"}
