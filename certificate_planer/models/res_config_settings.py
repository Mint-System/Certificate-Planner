from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tpi_page_text = fields.Char(config_parameter='certificate_planer.tpi_page_text')

    title_page_text = fields.Char(config_parameter='certificate_planer.title_page_text')

    footer_text = fields.Char(config_parameter='certificate_planer.footer_text')

    design_organisation_statement_text = fields.Char(config_parameter='certificate_planer.design_organisation_statement_text')

    dcc_survey_template_id = fields.Many2one('survey.survey', related='company_id.dcc_survey_template_id', readonly=False)

    occ_survey_template_id = fields.Many2one('survey.survey', related='company_id.occ_survey_template_id', readonly=False)

    conclusion_survey_template_id = fields.Many2one('survey.survey', related='company_id.conclusion_survey_template_id', readonly=False)
