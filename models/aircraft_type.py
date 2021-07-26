from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AircraftType(models.Model):
    _name = 'certificate_planer.aircraft_type'
    _description = 'Certificate Planner Aircraft Type'
    
    # fields
    active = fields.Boolean(default=True)
    name = fields.Char(required=True, string="Title")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Aircraft Type with this Title already exists."),
    ]
