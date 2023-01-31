from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class Part(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.part'
    _description = 'Certificate Planner Part'
    _order = 'name'
    
    name = fields.Char(required=True, string="Partnumber")
    designation = fields.Char(required=True)
    bom_id = fields.Many2one("certificate_planer.bom", string="BoM", store=False, compute="_compute_get_bom_id")
    certificate_id = fields.Many2one("certificate_planer.certificate", store=False, compute="_compute_get_certificate_id")

    part_ids = fields.One2many(related='bom_id.part_ids', string="Child Parts")
    part_count = fields.Integer(compute='_compute_part_count')

    prerequisite_ids = fields.One2many(related='bom_id.prerequisite_ids', string="Prerequisites")
    prerequisite_count = fields.Integer(compute='_compute_prerequisite_count')

    parent_bom_ids = fields.Many2many("certificate_planer.bom",
        relation="certificate_planer_bom_certificate_planer_part_rel",
        string="Parent BoMs",
        ondelete="restrict")
    parent_bom_count = fields.Integer(compute='_compute_parent_bom_count')

    prequisite_bom_ids = fields.Many2many("certificate_planer.bom",
        relation="certificate_planer_bom_certificate_planer_prerequisite_rel",
        string="Prerequisite for",
        ondelete="restrict")
    prerequisite_bom_count = fields.Integer(compute='_compute_prerequisite_bom_count')

    document_ids = fields.Many2many("certificate_planer.document", string="Documents", ondelete="restrict")
    document_count = fields.Integer(compute='_compute_document_count')

    change_ids = fields.Many2many("certificate_planer.change", string="Changes", ondelete="restrict")
    
    category_ids = fields.Many2many("certificate_planer.part_category", string="Categories", ondelete="restrict")

    _sql_constraints = [
        ('name_unique', 'unique (name)', "Part with this Partnumber already exists."),
    ]

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
                "name": _("%s (Copy)") % self.name,
        })
        return super().copy(default=default)
    
    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()

    def _compute_part_count(self):
        for record in self:
            record.part_count = len(self.part_ids)

    def _compute_document_count(self):
        for record in self:
            record.document_count = len(self.document_ids)

    def _compute_prerequisite_count(self):
        for record in self:
            record.prerequisite_count = len(self.prerequisite_ids)

    def _compute_prerequisite_bom_count(self):
        for record in self:
            record.prerequisite_bom_count = len(self.prequisite_bom_ids)

    def _compute_parent_bom_count(self):
        for record in self:
            record.parent_bom_count = len(self.parent_bom_ids)

    def _compute_get_bom_id(self):
        for part in self:
            part.bom_id = self.env['certificate_planer.bom'].search([('part_id', '=', part.id)])

    def _compute_get_certificate_id(self):
        self.certificate_id = self.env['certificate_planer.certificate'].search([('part_id','=',self.id)])

    def view_document_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Documents",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.document",
            "domain": [("id", "in", [t.id for t in self.document_ids])],
            "context": "{'create': False}",
        }

    def view_part_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Child Parts",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.part",
            "domain": [("id", "in", [t.certificate_planer_part_id.id for t in self.part_ids])],
            "context": "{'create': False}",
        }

    def view_prerequisite_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Prerequisites",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.part",
            "domain": [("id", "in", [t.certificate_planer_part_id.id for t in self.prerequisite_ids])],
            "context": "{'create': False}",
        }

    def view_parent_bom_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Parent BoMs",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.part",
            "domain": [("id", "in", [t.part_id.id for t in self.parent_bom_ids])],
            "context": "{'create': False}",
        }

    def view_prerequisite_bom_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Prerequisites for",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.part",
            "domain": [("id", "in", [t.part_id.id for t in self.prequisite_bom_ids])],
            "context": "{'create': False}",
        }