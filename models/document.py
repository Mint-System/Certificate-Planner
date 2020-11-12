# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Document(models.Model):
    _name = 'certificate_planer.document'
    _description = 'certificate_planer.document'

    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")
    current_revision_id = fields.Many2one("certificate_planer.document_revision", string="Current Revision")
    type_id = fields.Many2one("certificate_planer.document_type", string="Type")
    revision_ids = fields.One2many(
        "certificate_planer.document_revision",
        "document_id",
        "Revisions",
    )
    part_ids = fields.Many2many("certificate_planer.part", string="Parts")