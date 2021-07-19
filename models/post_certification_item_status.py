from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PostCertificationItemStatus(models.Model):
    _name = 'certificate_planer.post_certification_item_status'
    _description = 'Certificate Planner Post Certification Item Status'
    _rec_name = 'designation'
    _order = 'sequence'

    # fields
    designation = fields.Char()
    sequence = fields.Integer()
