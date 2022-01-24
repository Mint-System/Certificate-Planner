from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PartCategory(models.Model):
    _name = 'certificate_planer.part_category'
    _description = 'Certificate Planner Part Categroy'

    # fields
    active = fields.Boolean(default=True)
    name = fields.Char(required=True, string="Title")
    description = fields.Char()

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()