# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Bom(models.Model):
    _name = 'certificate_planer.bom'
    _description = 'Certificate Planer BoM'
    _rec_name = 'part_id'
    
    part_id = fields.Many2one("certificate_planer.part", required=True, string="Part")
    part_ids = fields.Many2many("certificate_planer.part", string="Parts")

    def unlink(self):
        self.part_id.unlink()
        return super(Bom, self).unlink()