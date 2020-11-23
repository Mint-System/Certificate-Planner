# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Part(models.Model):
    _name = 'certificate_planer.part'
    _description = 'Certificate Planer Part'

    # fields
    name = fields.Char(required=True, string="Title")
    description = fields.Char(required=True, string="Description")
    bom_ids = fields.Many2many("certificate_planer.bom", string="Parent BoMs")
    bom_id = fields.One2many("certificate_planer.bom", "part_id", string="BoM")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Part with this Title already exists."),
    ]

    def unlink(self):
        if len(self.bom_ids) != 0:
            raise UserError(_('You cannot delete a Part as long it is referenced by a parent BoM.'))
        return super(Part, self).unlink()