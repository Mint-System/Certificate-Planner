from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Document(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.document'
    _description = 'Certificate Planner Document'

    # fields
    name = fields.Char(required=True, string="Document ID")
    title = fields.Char(required=True)
    description = fields.Char(help="Document ID Assignment")
    revision_count = fields.Integer(compute='_compute_revision_count')

    current_revision_id = fields.Many2one("certificate_planer.document_revision", string="Current Revision", domain="[('document_id','=',id)]", track_visibility="always")
    change_id = fields.Many2one("certificate_planer.change", string="Change", track_visibility="always", ondelete="restrict")
    type_id = fields.Many2one("certificate_planer.document_type", required=True, string="Type", track_visibility="always", ondelete="restrict")
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate", track_visibility="always")
    state_id = fields.Many2one(related='current_revision_id.state_id')

    part_ids = fields.Many2many("certificate_planer.part", string="Parts", ondelete="restrict")

    revision_ids = fields.One2many("certificate_planer.document_revision", "document_id", string="Revisions", domain="[('document_id','=',id)]")

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document with this Document ID already exists."),
    ]
    
    # compute
    def _compute_revision_count(self):
        for record in self:
            record.revision_count = self.env['certificate_planer.document_revision'].search_count([('document_id', '=', self.id)])

    # actions
    def view_document_report(self):
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/certificate_planer.document_report_view/%(document_id)s' % {'document_id': self.id},
        }

    def view_document_revisions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Document Revisions',
            'view_mode': 'tree',
            'res_model': 'certificate_planer.document_revision',
            'domain': [('document_id', '=', self.id)],
            'context': "{'create': False}"
        }