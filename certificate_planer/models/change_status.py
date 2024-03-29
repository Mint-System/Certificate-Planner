from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ChangeStatus(models.Model):
    _name = 'certificate_planer.change_status'
    _description = 'Certificate Planner Change Status'
    _rec_name = 'designation'
    _order = 'sequence'

    # fields
    active = fields.Boolean(default=True)
    designation = fields.Char()
    sequence = fields.Integer()
    description = fields.Char()
    show_on_report = fields.Boolean("Show on MDL2 report")
    hide_legacy_class = fields.Boolean()
    hide_partnumbers = fields.Boolean("Hide Partnumbers")
    
    class_ids = fields.Many2many("certificate_planer.document_class", relation='certificate_planer_change_status_document_class_rel', string="Filter Document Classes")

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()