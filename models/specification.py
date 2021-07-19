from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Specification(models.Model):
    _name = 'certificate_planer.specification'
    _description = 'Certificate Planner Specification'
    
    # fields
    name = fields.Char(required=True, string="Title")
    certificate_ids = fields.One2many("certificate_planer.certificate", "specification_id", string="Certificates")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Specification with this Title already exists."),
    ]

    def unlink(self):
        if len(self.certificate_ids) != 0:
            raise UserError(_('You cannot delete a Specification as long it is referenced by a Certificate.'))
        return super(Specification, self).unlink()