# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Document(models.Model):
    _inherit = 'mail.thread'
    _name = 'certificate_planer.document'
    _description = 'Certificate Planer Document'

    # fields
    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")
    current_revision_id = fields.Many2one("certificate_planer.document_revision", string="Current Revision")
    type_id = fields.Many2one("certificate_planer.document_type", string="Type")
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate")
    revision_ids = fields.One2many("certificate_planer.document_revision","document_id",string="Revisions")
    part_ids = fields.Many2many("certificate_planer.part", string="Parts")
    issue_id = fields.Many2one("certificate_planer.issue", string="Issue")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document with this Title already exists."),
    ]