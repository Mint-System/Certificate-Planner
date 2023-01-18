from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    dcc_survey_template_id = fields.Many2one('survey.survey', domain="[('is_certificate_planner', '=', True)]")
    occ_survey_template_id = fields.Many2one('survey.survey', domain="[('is_certificate_planner', '=', True)]")
    conclusion_survey_template_id = fields.Many2one('survey.survey', domain="[('is_certificate_planner', '=', True)]")
