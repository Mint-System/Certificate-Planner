# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Document(models.Model):
    _inherit = 'mail.thread'
    _name = 'certificate_planer.document'
    _description = 'Certificate Planer Document'

    # fields
    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")
    current_revision_id = fields.Many2one("certificate_planer.document_revision", string="Current Revision", domain="[('document_id','=',id)]")
    issue_id = fields.Many2one("certificate_planer.issue", string="Issue")
    type_id = fields.Many2one("certificate_planer.document_type", required=True, string="Type")
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate")
    revision_ids = fields.One2many("certificate_planer.document_revision", "document_id", string="Revisions", domain="[('document_id','=',id)]")
    part_ids = fields.Many2many("certificate_planer.part", string="Parts")

    def unlink(self):
        if len(self.part_ids) != 0:
            raise UserError(_('You cannot delete a Document as long it is referenced by a Part.'))
        if len(self.revision_ids) != 0:
            raise UserError(_('You cannot delete a Document as long it is referenced by a Document Revision.'))
        return super(Document, self).unlink()