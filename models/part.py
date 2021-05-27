from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Part(models.Model):
    _inherit = 'mail.thread'
    _name = 'certificate_planer.part'
    _description = 'Certificate Planer Part'
    _order = 'sequence,name'
    
    # fields
    name = fields.Char(required=True, string="Title")
    sequence = fields.Integer(string="Sequence")
    description = fields.Char(required=True, string="Description")
    bom_ids = fields.Many2many("certificate_planer.bom", string="Parent BoMs")
    bom_id = fields.Many2one("certificate_planer.bom", string="BoM", store=False, compute="_get_bom_id")
    document_ids = fields.Many2many("certificate_planer.document", string="Documents")
    part_ids = fields.Many2many("certificate_planer.part", string="Child Parts", store=False, compute="_get_part_ids")


    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Part with this Title already exists."),
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
            res.append((rec.id, _('%s (%s)') % (rec.name, rec.description)))
        return res

    # compute
    def _get_bom_id(self):
        self.bom_id = self.env['certificate_planer.bom'].search([('part_id','=',self.id)])

    def _get_part_ids(self):
        self.part_ids = self.env['certificate_planer.bom'].search([('part_id','=',self.id)]).part_ids