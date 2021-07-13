from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IssueGroup(models.Model):
    _name = 'certificate_planer.issue_group'
    _description = 'Certificate Planer Issue Group'
    
    # fields
    name = fields.Char(required=True, string="Title")
    change_ids = fields.One2many("certificate_planer.change", "change_id", string="Changes")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Issue Group with this Title already exists."),
    ]

    def unlink(self):
        if len(self.change_ids) != 0:
            raise UserError(_('You cannot delete an Issue Group as long it is referenced by an Issue.'))
        return super(IssueGroup, self).unlink()