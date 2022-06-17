from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PostCertificationItem(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.post_certification_item'
    _description = 'Certificate Planner Post Certification Item'
    _rec_name = 'pci_id'
    
    # fields
    pci_id = fields.Char(string="PCI ID", required=True)
    description = fields.Char(required=True)

    change_id = fields.Many2one("certificate_planer.change", string="Change", ondelete="restrict")
    status_id = fields.Many2one("certificate_planer.post_certification_item_status", tracking=True, default=lambda self: self.env['certificate_planer.post_certification_item_status'].search([]), ondelete="restrict")

    # defaults
    def unlink(self):
        if self.change_id:
            raise UserError(_('You cannot delete a Post Certification Item that links to a Change.'))
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super(PostCertificationItem, self).unlink()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, f'{rec.pci_id} ({rec.change_id.change_id_id.name})'))
        return res
