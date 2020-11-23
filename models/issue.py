# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Issue(models.Model):
    _name = 'certificate_planer.issue'
    _description = 'Certificate Planer Issue'

    # fields
    name = fields.Char(required=True, string="Title")
    certificate_id = fields.Many2one("certificate_planer.certificate", required=True, string="Certificate")
    authority_number = fields.Char(required=True, string="Authority Number")
    project_number = fields.Char(required=True, string="Project Number")
    group_id = fields.Many2one("certificate_planer.issue_group", required=True, string="Group")
    revision_ids = fields.One2many("certificate_planer.document_revision", "issue_id", string="Document Revisions")
    document_ids = fields.One2many("certificate_planer.document", "issue_id", string="Documents")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Issue with this Title already exists."),
    ]

    def unlink(self):
        if len(self.document_ids) != 0:
            raise UserError(_('You cannot delete an Issue as long it is referenced by a Document.'))
        if len(self.revision_ids) != 0:
            raise UserError(_('You cannot delete an Issue as long it is referenced by a Document Revision.'))
        return super(Issue, self).unlink()