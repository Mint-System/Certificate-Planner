from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Change(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.change'
    _description = 'Certificate Planer Change'
    _rec_name = 'change_id_id'

    # fields
    description = fields.Char(required=True)
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate", track_visibility="always")
    authority_reference = fields.Char()
    reference = fields.Char(string="Aerolite Reference")
    change_id_id = fields.Many2one("certificate_planer.change_id", required=True, string="Change ID", track_visibility="always")
    revision_ids = fields.One2many("certificate_planer.document_revision", "change_id", string="Document Revisions")
    document_ids = fields.One2many("certificate_planer.document", "change_id", string="Documents")
    status_id = fields.Many2one("certificate_planer.change_status", track_visibility="always", ondelete='restrict')

    def unlink(self):
        if len(self.document_ids) != 0:
            raise UserError(_('You cannot delete an Change as long it is referenced by a Document.'))
        if len(self.revision_ids) != 0:
            raise UserError(_('You cannot delete an Change as long it is referenced by a Document Revision.'))
        return super(Change, self).unlink()

    # defaults
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s (%s)') % (rec.change_id_id.name, rec.certificate_id.part_id.name)))
        return res

    # @api.model
    # def _read_group_status_ids(self, statuses, domain, order):
    #     statuse_ids = statuses._search([], order=order)
    #     return statuses.browse(statuse_ids)