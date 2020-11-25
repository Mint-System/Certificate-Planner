# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DocumentRevision(models.Model):
    _name = 'certificate_planer.document_revision'
    _description = 'Certificate Planer Document Revision'
    _rec_name = 'document_id'

    # fields
    # name = fields.Char(required=True, string="Title")
    reason = fields.Text(required=True, string="Reason")
    document_id = fields.Many2one("certificate_planer.document", string="Document")
    state_id = fields.Many2one("certificate_planer.document_revision_state", required=True, string="State")
    issue_id = fields.Many2one("certificate_planer.issue", string="Issue")

    # defaults
    def name_get(self):
        result = []
        for record in self:
            record_name = record.document_id.name + ' - ' + record.state_id.name
            result.append((record.id, record_name))
        return result