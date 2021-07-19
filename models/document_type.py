from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentType(models.Model):
    _name = 'certificate_planer.document_type'
    _description = 'Certificate Planner Document Type'
    _rec_name = 'identification'

    # fields
    designation = fields.Char(required=True)
    identification = fields.Char(required=True)
    description = fields.Char(help="Document ID Assignment")
    document_ids = fields.One2many("certificate_planer.document", "type_id", string="Documents")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Type with this Title already exists."),
    ]

    def unlink(self):
        if len(self.document_ids) != 0:
            raise UserError(_('You cannot delete a Document Type as long it is referenced by a Document.'))
        return super(DocumentType, self).unlink()

    # defaults
    # def name_get(self):
    #     res = []
    #     for rec in self:
    #         res.append((rec.id, _('%s (%s)') % (rec.identification, rec.name)))
    #     return res