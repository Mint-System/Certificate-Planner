# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IssueGroup(models.Model):
    _name = 'certificate_planer.issue_group'
    _description = 'Certificate Planer Issue Group'
    
    name = fields.Char(required=True, string="Title")