# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DocumentRevision(models.Model):
    _name = 'certificate_planer.document.revision'
    _description = 'certificate_planer.document.revision'

    name = fields.Char(required=True, string="Title")
    document_id = fields.Many2one("certificate_planer.document", string="Document")

class Document(models.Model):
    _name = 'certificate_planer.document'
    _description = 'certificate_planer.document'

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    revision_ids = fields.One2many(
        "certificate_planer.document.revision",
        "document_id",
        "Revisions",
    )
    part_ids = fields.Many2many("certificate_planer.part", string="Parts")

class Part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'certificate_planer.part'

    name = fields.Char(required=True, string="Title")
    number = fields.Char(required=True, string="Number")
    # bom_id = fields.Many2one("certificate_planer.bom", "BoM")

class Bom(models.Model):
    _name = 'certificate_planer.bom'
    _description = 'certificate_planer.bom'
    _rec_name = 'part_id'
    
    part_id = fields.Many2one("certificate_planer.part", string="Part")
    part_ids = fields.Many2many("certificate_planer.part", string="Parts")