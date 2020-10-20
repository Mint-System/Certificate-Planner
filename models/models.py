# -*- coding: utf-8 -*-

from odoo import models, fields, api

class revision(models.Model):
    _name = 'certificate_planer.document.revision'
    _description = 'certificate_planer.document.revision'

    name = fields.Char(required=True, string="Title")
    document_id = fields.Many2one("certificate_planer.document", "Document")

class document(models.Model):
    _name = 'certificate_planer.document'
    _description = 'certificate_planer.document'

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    revision_ids = fields.One2many(
        "certificate_planer.document.revision",
        "document_id",
        "Revisions",
    )
    part_ids = fields.Many2many('certificate_planer.part', string="Parts")

class part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'certificate_planer.part'

    name = fields.Char(required=True, string="Title")

    parent_id = fields.Many2one('certificate_planer.part', string='BOM ID')
    child_ids = fields.One2many(
         'certificate_planer.part',
         'parent_id',
         string='BOM'
    )
