# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'certificate_planer.part'

    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")
    bom_ids = fields.Many2many("certificate_planer.bom", string="Parent BoMs")
    bom_id = fields.One2many("certificate_planer.bom", "part_id", string="BoM")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents")
