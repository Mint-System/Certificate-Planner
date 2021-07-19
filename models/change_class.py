from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeClass(models.Model):
    _name = 'certificate_planer.change_class'
    _description = 'Certificate Planner Change Class'
    _rec_name = 'designation'

    # fields
    designation = fields.Char()
    description = fields.Char()
