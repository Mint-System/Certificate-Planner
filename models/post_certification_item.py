from odoo import models, fields, api, _

class PostCertificationItem(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.post_certification_item'
    _description = 'Certificate Planner Post Certification Item'
    _rec_name = 'pci_id'
    
    # fields
    pci_id = fields.Char(string="PCI ID", require=True)
    description = fields.Char(required=True)
    change_id = fields.Many2one("certificate_planer.change", required=True, string="Change")
    status_id = fields.Many2one("certificate_planer.post_certification_item_status", track_visibility="always", ondelete='restrict', default=lambda self: self.env['certificate_planer.post_certification_item_status'].search([]))

    # defaults
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, f'{rec.pci_id} ({rec.change_id.change_id_id.name})'))
        return res