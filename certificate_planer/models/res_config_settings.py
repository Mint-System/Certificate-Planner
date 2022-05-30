from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tpi_page_text = fields.Char(config_parameter='certificate_planer.tpi_page_text',
                                default="This Index is approved with DOCUMENT_NAME DOCUMENT_REVISION_TITLE.",
                                help="The placeholder DOCUMENT_NAME and DOCUMENT_REVISION_TITLE are populated when generating the report.")

    title_page_text = fields.Char(config_parameter='certificate_planer.title_page_text',
                                  default="This document contains confidential information and is proprietary to Aerolite AG. It may not be disclosed, reproduced or utilised in any way, in whole or in part, without the written consent of Aerolite AG.")

    footer_text = fields.Char(config_parameter='certificate_planer.footer_text',
                              default="Copyright by Aerolite AG, Aumühlestrasse 10, CH-6373 Ennetbürgen")

    design_organisation_statement_text = fields.Char(config_parameter='certificate_planer.design_organisation_statement_text',
                                                     default="Approved under the authority of the Design Organisation No: EASA.21J.359")
