from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentClass(models.Model):
    _name = 'certificate_planer.document_class'
    _description = 'Certificate Planner Document Class'
    _order = 'sequence'

    # fields
    active = fields.Boolean(default=True)
    sequence = fields.Integer()
    name = fields.Char(required=True, string="Title")
    description = fields.Char(help="Document ID Assignment")
    show_on_report = fields.Boolean("Show on MDL2 report")
    show_on_tpi_report = fields.Boolean("Show on TPI report")
    show_reason = fields.Boolean()
    mcr_planning = fields.Boolean("MCR Planning")
    mcr_design = fields.Boolean("MCR Inst. and Design")

    status_ids = fields.Many2many("certificate_planer.change_status", relation='certificate_planer_change_status_document_class_rel', string="Filter Change Status")

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()