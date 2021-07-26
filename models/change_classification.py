from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeClassification(models.Model):
    _name = 'certificate_planer.change_classification'
    _description = 'Certificate Planner Change Classification'
    _rec_name = 'designation'

    # fields
    active = fields.Boolean(default=True)
    designation = fields.Char()
    description = fields.Char()
