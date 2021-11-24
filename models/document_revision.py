from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentRevision(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.document_revision'
    _description = 'Certificate Planner Document Revision'
    _rec_name = 'document_id'
    _order = 'index_id'

    # fields
    reason = fields.Text(required=True)

    current_revision_id = fields.Many2one(related="document_id.current_revision_id", string="Current Revision")
    title = fields.Char(related="document_id.title", string="Title")
    type_id = fields.Many2one(related="document_id.type_id", string="Type")
    document_id = fields.Many2one("certificate_planer.document", string="Document", track_visibility="always", ondelete="restrict")
    index_id = fields.Many2one("certificate_planer.document_revision_index", required=True, string="Index", track_visibility="always", ondelete="restrict")
    change_id = fields.Many2one("certificate_planer.change", string="Change", track_visibility="always", ondelete="restrict")
    change_status_id = fields.Many2one(related='change_id.status_id')

    # defaults
    def unlink(self):
        is_current_revision = self.document_id.current_revision_id == self
        if is_current_revision:
            raise UserError(_('You cannot delete a Document Revision as long it is set as Current Revision.'))
        return super(DocumentRevision, self).unlink()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s') % (rec.index_id.name)))
        return res
