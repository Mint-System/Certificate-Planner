from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    is_certificate_planner = fields.Boolean(string="Certificate Planner",
        help="Make answers of this survey available to Certificate Planner changes.")

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    change_id = fields.Many2one("certificate_planer.change", string="Change")

    def name_get(self):
        res = []
        user = self.env.user
        for rec in self:           
            create_date = fields.Datetime.context_timestamp(user, rec.create_date).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            res.append((rec.id, '%(title)s on %(create_date)s by %(partner)s' % {
                'title': rec.survey_id.title,
                'create_date': create_date,
                'partner': rec.partner_id.display_name
            }))
        return res