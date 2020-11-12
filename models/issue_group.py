# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IssueGroup(models.Model):
    _name = 'certificate_planer.issue_group'
    _description = 'certificate_planer.issue_group'
    
    name = fields.Char(required=True, string="Title")