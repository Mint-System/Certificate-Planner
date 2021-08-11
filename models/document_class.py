from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentClass(models.Model):
    _name = 'certificate_planer.document_class'
    _description = 'Certificate Planner Document Class'
    _order = 'sequence'

    # fields
    active = fields.Boolean(default=True)
    sequence = fields.Integer()
    name = fields.Char(required=True, string="Title")
    description = fields.Char(help="Document ID Assignment")
