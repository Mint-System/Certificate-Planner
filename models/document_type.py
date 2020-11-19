# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DocumentType(models.Model):
    _name = 'certificate_planer.document_type'
    _description = 'Certificate Planer Document Type'
    
    # fields
    name = fields.Char(required=True, string="Title")
    abbreviation = fields.Char(required=True, string="Abbreviation")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name,abbreviation)', "Document Type with this Title and/or Abbreviation already exists."),
    ]