from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class Part(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.part'
    _description = 'Certificate Planner Part'
    _order = 'name'
    
    # fields
    name = fields.Char(required=True, string="Partnumber")
    designation = fields.Char(required=True)
    part_count = fields.Integer(compute='_compute_part_count')
    prerequisite_count = fields.Integer(compute='_compute_prerequisite_count')

    bom_id = fields.Many2one("certificate_planer.bom", string="BoM", store=False, compute="_compute_get_bom_id")
    certificate_id = fields.Many2one("certificate_planer.certificate", store=False, compute="_compute_get_certificate_id")

    part_ids = fields.One2many(related='bom_id.part_ids', string="Child Parts")
    prerequisite_ids = fields.One2many(related='bom_id.prerequisite_ids', string="Prerequisites")
    
    parent_bom_ids = fields.Many2many("certificate_planer.bom", relation="certificate_planer_bom_certificate_planer_part_rel", string="Parent BoMs", ondelete="restrict")
    prequisite_bom_ids = fields.Many2many("certificate_planer.bom", relation="certificate_planer_bom_certificate_planer_prerequisite_rel", string="Prerequisite for", ondelete="restrict")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents", ondelete="restrict")
    change_ids = fields.Many2many("certificate_planer.change", string="Changes", ondelete="restrict")
    category_ids = fields.Many2many("certificate_planer.part_category", string="Categories", ondelete="restrict")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Part with this Partnumber already exists."),
    ]

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s (%s)') % (rec.name, rec.designation)))
        return res

    # compute
    def _compute_part_count(self):
        for record in self:
            record.part_count = len(self.part_ids)

    def _compute_prerequisite_count(self):
        for record in self:
            record.prerequisite_count = len(self.prerequisite_ids)

    def _compute_get_bom_id(self):
        self.bom_id = self.env['certificate_planer.bom'].search([('part_id','=',self.id)])

    def _compute_get_certificate_id(self):
        self.certificate_id = self.env['certificate_planer.certificate'].search([('part_id','=',self.id)])

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