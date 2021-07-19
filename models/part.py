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
    bom_ids = fields.Many2many("certificate_planer.bom", string="Parent BoMs")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents")
    part_ids = fields.Many2many("certificate_planer.part", string="Child Parts", store=False, compute="_compute_get_part_ids")
    # Inverted fiels without One2many
    bom_id = fields.Many2one("certificate_planer.bom", string="BoM", store=False, compute="_compute_get_bom_id")
    certificate_id = fields.Many2one("certificate_planer.certificate", store=False, compute="_compute_get_certificate_id")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Part with this Partnumber already exists."),
    ]

    def unlink(self):
        if len(self.bom_ids) != 0:
            raise UserError(_('You cannot delete a BoM/Part as long it is referenced by a parent BoM.'))
        if len(self.document_ids) != 0:
            raise UserError(_('You cannot delete a BoM/Part as long it is referenced by a document.'))
        return super(Part, self).unlink()

    # defaults
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