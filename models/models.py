# -*- coding: utf-8 -*-

from odoo import models, fields, api


class document(models.Model):
    _name = 'certificate_planer.document'
    _description = 'certificate_planer.document'

    title = fields.Char(required=True)
    part_ids = fields.Many2many('certificate_planer.part', string="Parts")
    description = fields.Text()

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'certificate_planer.part'

    title = fields.Char(required=True)
    bom_id = fields.Many2one('certificate_planer.part', string='BOM ID')

    bom_ids = fields.One2many(
         'certificate_planer.part',
         'bom_id',
         string='BOM'
    )
