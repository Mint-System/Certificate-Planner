# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'certificate_planer.part'

    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")