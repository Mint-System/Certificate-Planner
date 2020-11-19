# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class DocumentRevisionState(models.Model):
    _name = 'certificate_planer.document_revision_state'
    _description = 'Certificate Planer Document Revision State'
    
    # field
    name = fields.Char(required=True, string="Title")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document Revision State with this Title already exists."),
    ]