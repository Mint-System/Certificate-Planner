# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DocumentRevisionState(models.Model):
    _name = 'certificate_planer.document_revision_state'
    _description = 'Certificate Planer Document Revision State'
    
    name = fields.Char(required=True, string="Title")