from odoo import models, fields, api


class Bom(models.Model):
    _name = 'certificate_planer.bom'
    _description = 'Certificate Planner BoM'
    _rec_name = 'part_id'
    
    # fields
    part_id = fields.Many2one("certificate_planer.part", string="Part")
    part_ids = fields.One2many(
        "certificate_planer.bom_certificate_planer_part_rel",
        "certificate_planer_bom_id",
        string="Child Parts",
    )
    prerequisite_ids = fields.One2many(
        "certificate_planer.bom_certificate_planer_prerequisite_rel",
        "certificate_planer_bom_id",
        string="Prerequisites",
    )

    # constraints
    _sql_constraints = [
        ('part_id_unique', 'unique (part_id)', "BoM with this Part already exists."),
    ]

    # defaults
    def unlink(self):
        self.part_id.unlink()
        return super(Bom, self).unlink()

class BomPartRel(models.Model):
    _name = "certificate_planer.bom_certificate_planer_part_rel"
    _description = "Certificate Planner BoM Parent Relation"
    _order = 'sequence'
    _rec_name = 'certificate_planer_bom_id'

    designation = fields.Char(related='certificate_planer_part_id.designation')

    certificate_planer_bom_id = fields.Many2one("certificate_planer.bom", string="BoM")
    certificate_planer_part_id = fields.Many2one("certificate_planer.part", string="Part")

    # constraints
    _sql_constraints = [
        ('bom_part_unique', 'UNIQUE (certificate_planer_bom_id, certificate_planer_part_id)', "Relation with this BoM and Part already exists."),
        ('self_ref_check', 'CHECK (certificate_planer_bom_id <> certificate_planer_part_id)', "BoM cannot have linked Part as Child Part."),
    ]

    # fields
    sequence = fields.Integer()

class BomPrerequisiteRel(models.Model):
    _name = "certificate_planer.bom_certificate_planer_prerequisite_rel"
    _description = "Certificate Planner BoM Prerequisite Relation"
    _order = 'sequence'
    _rec_name = 'certificate_planer_bom_id'

    designation = fields.Char(related='certificate_planer_part_id.designation')

    certificate_planer_bom_id = fields.Many2one("certificate_planer.bom", string="BoM")
    certificate_planer_part_id = fields.Many2one("certificate_planer.part", string="Prerequisite")

    # constraints
    _sql_constraints = [
        ('bom_prerequisite_unique', 'UNIQUE (certificate_planer_bom_id, certificate_planer_part_id)', "Relation with this BoM and Prerequisite already exists."),
        ('self_ref_check', 'CHECK (certificate_planer_bom_id <> certificate_planer_part_id)', "BoM cannot have linked Part as Prerequisite."),
    ]

    # fields
    sequence = fields.Integer()