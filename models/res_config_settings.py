from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    title_page_text = fields.Char(config_parameter='certificate_planer.title_page_text',
        default="This document contains confidential information and is proprietary to Aerolite AG. It may not be disclosed, reproduced or utilised in any way, in whole or in part, without the written consent of Aerolite AG.")
    
    footer_text = fields.Char(config_parameter='certificate_planer.footer_text',
        default="Copyright by Aerolite AG, Aumühlestrasse 10, CH-6373 Ennetbürgen")