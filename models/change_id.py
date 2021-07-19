from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ChangeID(models.Model):
    _name = 'certificate_planer.change_id'
    _description = 'Certificate Planner Change ID'
    
    # fields
    name = fields.Char(required=True, string="Title")
    change_ids = fields.One2many("certificate_planer.change", "change_id_id", string="Changes")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Change ID with this Title already exists."),
    ]

    def unlink(self):
        if len(self.change_ids) != 0:
            raise UserError(_('You cannot delete an Change ID as long it is referenced by a Change.'))
        return super(ChangeID, self).unlink()