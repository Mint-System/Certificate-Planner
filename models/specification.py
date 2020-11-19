# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Specification(models.Model):
    _name = 'certificate_planer.specification'
    _description = 'Certificate Planer Specification'
    
    # fields
    name = fields.Char(required=True, string="Title")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Specification with this Title already exists."),
    ]