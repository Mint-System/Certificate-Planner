# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Certificate(models.Model):
    _name = 'certificate_planer.certificate'
    _description = 'certificate_planer.certificate'

    name = fields.Char(required=True, string="Title")
    part_id = fields.Many2one("certificate_planer.part", string="Part")
    aircraft = fields.Char(required=True, string="Aircraft")
    specification_id = fields.Many2one("certificate_planer.specification", string="Specification")
