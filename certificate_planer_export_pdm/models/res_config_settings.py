from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    change_status_text = fields.Char(config_parameter='certificate_planer_export_pdm.change_status_text')
    change_status_confirm_text = fields.Char(config_parameter='certificate_planer_export_pdm.change_status_confirm_text')

    pdm_export_type = fields.Selection(
        config_parameter='certificate_planer_export_pdm.pdm_export_type',
        selection=[('file', 'File export'), ('attachment', 'Attachment')],
        default='attachment',
    )