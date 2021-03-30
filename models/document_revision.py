# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DocumentRevision(models.Model):
    _inherit = 'mail.thread'
    _name = 'certificate_planer.document_revision'
    _description = 'Certificate Planer Document Revision'
    _rec_name = 'document_id'

    # fields
    # name = fields.Char(required=True, string="Title")
    reason = fields.Text(required=True, string="Reason")
    document_id = fields.Many2one("certificate_planer.document", string="Document", track_visibility="always")
    state_id = fields.Many2one("certificate_planer.document_revision_state", required=True, string="State", track_visibility="always")
    issue_id = fields.Many2one("certificate_planer.issue", string="Issue", track_visibility="always")

    # defaults
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s') % (rec.state_id.name)))
        return res