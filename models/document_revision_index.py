from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentRevisionIndex(models.Model):
    _name = 'certificate_planer.document_revision_index'
    _description = 'Certificate Planner Document Revision Index'
    _order = 'sequence'

    # fields
    name = fields.Char(required=True, string="Index")
    active = fields.Boolean(default=True)
    sequence = fields.Integer()

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Revision Index with this Index already exists."),
    ]

    # defaults
    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = [('name', "like", name)]
        
        records = self.search(domain + args, limit=limit)
        return records.name_get()
