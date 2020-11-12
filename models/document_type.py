# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DocumentType(models.Model):
    _name = 'certificate_planer.document_type'
    _description = 'certificate_planer.document_type'
    
    name = fields.Char(required=True, string="Title")
    abbreviation = fields.Char(required=True, string="Abbreviation")