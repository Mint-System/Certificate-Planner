from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeID(models.Model):
    _name = 'certificate_planer.change_id'
    _description = 'Certificate Planner Change ID'
    _order = 'sequence'

    # fields
    name = fields.Char(required=True, string="Title")
    sequence = fields.Integer()

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Change ID with this Title already exists."),
    ]
