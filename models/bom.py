from odoo import models, fields, api

class Bom(models.Model):
    _name = 'certificate_planer.bom'
    _description = 'Certificate Planer BoM'
    _rec_name = 'part_id'
    
    # fields
    part_id = fields.Many2one("certificate_planer.part", string="Part")
    part_ids = fields.Many2many("certificate_planer.part", string="Child Parts")

    # constraints
    _sql_constraints = [
        ('part_id_unique', 'unique (part_id)', "BoM with this Part already exists."),
    ]

    def unlink(self):
        self.part_id.unlink()
        return super(Bom, self).unlink()