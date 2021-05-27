from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Issue(models.Model):
    _inherit = 'mail.thread'
    _name = 'certificate_planer.issue'
    _description = 'Certificate Planer Issue'
    _rec_name = 'group_id'

    # fields
    description = fields.Char(required=True, string="Description")
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate", track_visibility="always")
    authority_number = fields.Char(string="Authority Number")
    project_number = fields.Char(string="Project Number")
    group_id = fields.Many2one("certificate_planer.issue_group", required=True, string="Group", track_visibility="always")
    revision_ids = fields.One2many("certificate_planer.document_revision", "issue_id", string="Document Revisions")
    document_ids = fields.One2many("certificate_planer.document", "issue_id", string="Documents")

    def unlink(self):
        if len(self.document_ids) != 0:
            raise UserError(_('You cannot delete an Issue as long it is referenced by a Document.'))
        if len(self.revision_ids) != 0:
            raise UserError(_('You cannot delete an Issue as long it is referenced by a Document Revision.'))
        return super(Issue, self).unlink()

    # defaults
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s (%s)') % (rec.group_id.name, rec.certificate_id.part_id.name)))
        return res