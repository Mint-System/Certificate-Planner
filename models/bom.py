from odoo import models, fields, api

class Bom(models.Model):
    _name = 'certificate_planer.bom'
    _description = 'Certificate Planner BoM'
    _rec_name = 'part_id'
    
    # fields
    part_id = fields.Many2one("certificate_planer.part", string="Part")
    part_ids = fields.Many2many("certificate_planer.part", string="Child Parts", ondelete="restrict")
    prerequisite_ids = fields.One2many(
        "certificate_planer.bom_prerequisite_rel",
        "parent_id",
        string="Prerequisites",
    )
    # prerequisite_ids = fields.Many2many(
    #     comodel_name="certificate_planer.part",
    #     relation="certificate_planer_bom_prerequisite_rel",
    #     string="Prerequisites",
    #     ondelete="restrict",
    # )

    # constraints
    _sql_constraints = [
        ('part_id_unique', 'unique (part_id)', "BoM with this Part already exists."),
    ]

    # defaults
    def unlink(self):
        self.part_id.unlink()
        return super(Bom, self).unlink()

class BomPrerequisiteRel(models.Model):
    _name = "certificate_planer.bom_prerequisite_rel"
    _description = "Certificate Planner BoM Prerequisite Relation"
    _order = 'sequence'
    _rec_name = 'parent_id'

    parent_id = fields.Many2one("certificate_planer.bom", string="Parent")
    child_id = fields.Many2one("certificate_planer.part", string="Child")

    # fields
    sequence = fields.Integer()