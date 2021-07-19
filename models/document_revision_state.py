from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentRevisionState(models.Model):
    _name = 'certificate_planer.document_revision_state'
    _description = 'Certificate Planner Document Revision State'
    
    # fields
    name = fields.Char(required=True, string="Title")
    revision_ids = fields.One2many("certificate_planer.document_revision", "state_id", string="Document Revisions")
    active = fields.Boolean(default=True)
    
    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Revision State with this Title already exists."),
    ]

    # defaults
    def unlink(self):
        if len(self.revision_ids) != 0:
            raise UserError(_('You cannot delete a Document Revision State as long it is referenced by a Document Revision.'))
        return super(DocumentRevisionState, self).unlink()

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = [('name', "like", name)]
        
        records = self.search(domain + args, limit=limit)
        return records.name_get()
