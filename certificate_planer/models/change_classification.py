from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ChangeClassification(models.Model):
    _name = 'certificate_planer.change_classification'
    _description = 'Certificate Planner Change Classification'
    _rec_name = 'designation'

    # fields
    active = fields.Boolean(default=True)
    designation = fields.Char()
    description = fields.Char()

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()