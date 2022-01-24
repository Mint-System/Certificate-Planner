from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AircraftType(models.Model):
    _name = 'certificate_planer.aircraft_type'
    _description = 'Certificate Planner Aircraft Type'
    
    # fields
    active = fields.Boolean(default=True)
    name = fields.Char(required=True, string="Title")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Aircraft Type with this Title already exists."),
    ]

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()