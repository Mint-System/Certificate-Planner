# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Certificate(models.Model):
    _name = 'certificate_planer.certificate'
    _description = 'Certificate Planer Certificate'

    # fields
    name = fields.Char(required=True, string="Title")
    part_id = fields.Many2one("certificate_planer.part", string="Part")
    aircraft = fields.Char(required=True, string="Aircraft")
    specification_id = fields.Many2one("certificate_planer.specification", required=True, string="Specification")
    document_ids = fields.One2many("certificate_planer.document", "certificate_id", string="Documents")
    issue_ids = fields.One2many("certificate_planer.issue", "certificate_id", string="Issues")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Certificate with this Title already exists."),
    ]