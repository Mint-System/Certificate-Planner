from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PostCertificationItemStatus(models.Model):
    _name = 'certificate_planer.post_certification_item_status'
    _description = 'Certificate Planner Post Certification Item Status'
    _rec_name = 'designation'
    _order = 'sequence'

    # fields
    active = fields.Boolean(default=True)
    designation = fields.Char()
    sequence = fields.Integer()
    description = fields.Char()

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()