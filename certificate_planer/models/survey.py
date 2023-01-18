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

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%(title)s on %(datetime)s by %(partner)s' % {
                'title': rec.survey_id.title,
                'datetime': rec.create_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'partner': rec.partner_id.display_name
            }))
        return res