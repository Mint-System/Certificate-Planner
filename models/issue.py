# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Issue(models.Model):
    _name = 'certificate_planer.issue'
    _description = 'certificate_planer.issue'

    name = fields.Char(required=True, string="Title")
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate")
    authority_number = fields.Char(required=True, string="Authority Number")
    project_number = fields.Char(required=True, string="Project Number")
    group_id = fields.Many2one("certificate_planer.issue_group", string="Group")