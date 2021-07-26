from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentType(models.Model):
    _name = 'certificate_planer.document_type'
    _description = 'Certificate Planner Document Type'
    _rec_name = 'identification'

    # fields
    active = fields.Boolean(default=True)
    designation = fields.Char(required=True)
    identification = fields.Char(required=True)
    description = fields.Char(help="Document ID Assignment")
    
    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Type with this Title already exists."),
    ]
