from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    change_status_text = fields.Char(config_parameter='certificate_planer_export_pdm.change_status_text')
