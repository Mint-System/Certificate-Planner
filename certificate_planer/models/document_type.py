from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentType(models.Model):
    _name = 'certificate_planer.document_type'
    _description = 'Certificate Planner Document Type'
    _rec_name = 'identification'
    _order = 'sequence'

    # fields
    active = fields.Boolean(default=True)
    sequence = fields.Integer()

    designation = fields.Char(required=True)
    identification = fields.Char(required=True)
    description = fields.Char(help="Document ID Assignment")
    
    class_id = fields.Many2one("certificate_planer.document_class", string="Document Class", ondelete="restrict")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Type with this Title already exists."),
    ]

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()