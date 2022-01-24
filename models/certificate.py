from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Certificate(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.certificate'
    _description = 'Certificate Planner Certificate'
    _rec_name = 'part_id'
    
    # fields
    part_id = fields.Many2one("certificate_planer.part", required=True, string="Part")
    
    aircraft_type_id = fields.Many2one("certificate_planer.aircraft_type", required=True, string="Aircraft Type", track_visibility="always", ondelete="restrict")
    specification_id = fields.Many2one("certificate_planer.specification", required=True, string="Specification", track_visibility="always", ondelete="restrict")
    
    document_ids = fields.One2many("certificate_planer.document", "certificate_id", string="Documents")
    change_ids = fields.One2many("certificate_planer.change", "certificate_id", string="Changes")

    # constraints
    _sql_constraints = [
        ('part_id_unique', 'unique (part_id)', "Certificate with this Part already exists."),
    ]

    # defaults
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s (%s)') % (rec.part_id.name, rec.aircraft_type_id.name)))
        return res

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()