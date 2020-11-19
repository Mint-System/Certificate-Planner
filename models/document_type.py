# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DocumentType(models.Model):
    _name = 'certificate_planer.document_type'
    _description = 'Certificate Planer Document Type'
    
    name = fields.Char(required=True, string="Title")
    abbreviation = fields.Char(required=True, string="Abbreviation")