# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'Certificate Planer Part'

    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")
    bom_ids = fields.Many2many("certificate_planer.bom", string="Parent BoMs")
    bom_id = fields.One2many("certificate_planer.bom", "part_id", string="BoM")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents")

    _sql_constraints = [
        ('name_unique', 'unique (name)', "Part with this Title already exists."),
    ]