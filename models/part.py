from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Part(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.part'
    _description = 'Certificate Planner Part'
    _order = 'sequence,name'
    
    # fields
    name = fields.Char(required=True, string="Partnumber")
    sequence = fields.Integer()
    designation = fields.Char(required=True)

    bom_id = fields.Many2one("certificate_planer.bom", string="BoM", store=False, compute="_compute_get_bom_id")
    certificate_id = fields.Many2one("certificate_planer.certificate", store=False, compute="_compute_get_certificate_id")

    bom_ids = fields.Many2many("certificate_planer.bom", string="Parent BoMs", ondelete="restrict")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents", ondelete="restrict")
    change_ids = fields.Many2many("certificate_planer.change", string="Changes", ondelete="restrict")
    category_ids = fields.Many2many("certificate_planer.part_category", string="Categories", ondelete="restrict")
    part_ids = fields.Many2many("certificate_planer.part", string="Child Parts", store=False, compute="_compute_get_part_ids")

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
    def _compute_get_bom_id(self):
        self.bom_id = self.env['certificate_planer.bom'].search([('part_id','=',self.id)])

    def _compute_get_part_ids(self):
        self.part_ids = self.env['certificate_planer.bom'].search([('part_id','=',self.id)]).part_ids

    def _compute_get_certificate_id(self):
        self.certificate_id = self.env['certificate_planer.certificate'].search([('part_id','=',self.id)])