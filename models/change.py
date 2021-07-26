from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Change(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.change'
    _description = 'Certificate Planner Change'
    _rec_name = 'change_id_id'

    # fields
    description = fields.Char(required=True)
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate", track_visibility="always")
    authority_reference = fields.Char()
    reference = fields.Char(string="Aerolite Reference")

    status_id = fields.Many2one("certificate_planer.change_status", track_visibility="always", default=lambda self: self.env['certificate_planer.change_status'].search([]), ondelete="restrict")
    classification_id = fields.Many2one("certificate_planer.change_classification", track_visibility="always", default=lambda self: self.env['certificate_planer.change_classification'].search([]), ondelete="restrict")
    change_id_id = fields.Many2one("certificate_planer.change_id", required=True, string="Change ID", track_visibility="always", ondelete="restrict")
    
    part_ids = fields.Many2many("certificate_planer.part", string="Parts", ondelete="restrict")

    revision_ids = fields.One2many("certificate_planer.document_revision", "change_id", string="Document Revisions")
    item_ids = fields.One2many("certificate_planer.post_certification_item", "change_id", string="Post Certification Items")

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s (%s)') % (rec.change_id_id.name, rec.certificate_id.part_id.name)))
        return res
