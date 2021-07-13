from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentRevision(models.Model):
    _inherit = 'mail.thread'
    _name = 'certificate_planer.document_revision'
    _description = 'Certificate Planer Document Revision'
    _rec_name = 'document_id'

    # fields
    reason = fields.Text(required=True)
    document_id = fields.Many2one("certificate_planer.document", string="Document", track_visibility="always")
    state_id = fields.Many2one("certificate_planer.document_revision_state", required=True, string="State", track_visibility="always")
    change_id = fields.Many2one("certificate_planer.change", string="Change", track_visibility="always")

    # defaults
    def unlink(self):
        is_current_revision = self.document_id.current_revision_id == self
        if is_current_revision:
            raise UserError(_('You cannot delete a Document Revision as long it is set as Current Revision.'))
        return super(DocumentRevision, self).unlink()


    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s') % (rec.state_id.name)))
        return res
