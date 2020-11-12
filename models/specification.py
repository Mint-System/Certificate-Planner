# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Specification(models.Model):
    _name = 'certificate_planer.specification'
    _description = 'certificate_planer.specification'
    
    name = fields.Char(required=True, string="Title")