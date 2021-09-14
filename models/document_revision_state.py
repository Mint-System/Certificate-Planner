from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentRevisionState(models.Model):
    _name = 'certificate_planer.document_revision_state'
    _description = 'Certificate Planner Document Revision State'
    _order = 'sequence'

    # fields
    name = fields.Char(required=True, string="Title")
    active = fields.Boolean(default=True)
    sequence = fields.Integer()

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Revision State with this Title already exists."),
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
