from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AircraftType(models.Model):
    _name = 'certificate_planer.aircraft_type'
    _description = 'Certificate Planner Aircraft Type'
    
    # fields
    name = fields.Char(required=True, string="Title")
    certificate_ids = fields.One2many("certificate_planer.certificate", "aircraft_type_id", string="Certificates")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Aircraft Type with this Title already exists."),
    ]

    def unlink(self):
        if len(self.certificate_ids) != 0:
            raise UserError(_('You cannot delete a Aircraft Type as long it is referenced by a Certificate.'))
        return super(AircraftType, self).unlink()
