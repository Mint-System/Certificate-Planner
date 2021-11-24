from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ChangeStatus(models.Model):
    _name = 'certificate_planer.change_status'
    _description = 'Certificate Planner Change Status'
    _rec_name = 'designation'
    _order = 'sequence'

    # fields
    active = fields.Boolean(default=True)
    designation = fields.Char()
    sequence = fields.Integer()
    description = fields.Char()
    show_on_report = fields.Boolean("Show on MDL2 report")
    hide_legacy_class = fields.Boolean()