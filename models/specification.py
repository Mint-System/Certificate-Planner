from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Specification(models.Model):
    _name = 'certificate_planer.specification'
    _description = 'Certificate Planner Specification'
    
    # fields
    active = fields.Boolean(default=True)
    name = fields.Char(required=True, string="Title")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Specification with this Title already exists."),
    ]
