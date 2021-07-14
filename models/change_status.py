from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeStatus(models.Model):
    _name = 'certificate_planer.change_status'
    _description = 'Certificate Planer Change Status'
    _rec_name = 'designation'
    _order = 'sequence'

    # fields
    designation = fields.Char()
    sequence = fields.Integer()
