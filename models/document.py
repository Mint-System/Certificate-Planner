from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging
_logger = logging.getLogger(__name__)


class Document(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.document'
    _description = 'Certificate Planner Document'

    # fields
    name = fields.Char(required=True, string="Document ID")
    title = fields.Char(required=True)
    description = fields.Char(help="Document ID Assignment")
    revision_count = fields.Integer(compute='_compute_revision_count')
    attachment_count = fields.Integer(compute='_compute_attachment_count')
    print_date = fields.Datetime()
    current_revision_id = fields.Many2one("certificate_planer.document_revision", string="Current Revision", domain="[('document_id','=',id)]", track_visibility="always")
    change_id = fields.Many2one("certificate_planer.change", string="Change", readonly=True) # deprecated
    type_id = fields.Many2one("certificate_planer.document_type", required=True, string="Type", track_visibility="always", ondelete="restrict")
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate", track_visibility="always")
    index_id = fields.Many2one(related='current_revision_id.index_id')

    part_ids = fields.Many2many("certificate_planer.part", string="Parts", ondelete="restrict", read=['certificate_planer.group_certificate_planer_manager_document'])

    revision_ids = fields.One2many("certificate_planer.document_revision", "document_id", string="Revisions", domain="[('document_id','=',id)]", read=['certificate_planer.group_certificate_planer_manager_document'])

    # constraints
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Document with this Document ID already exists."),
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

    # compute
    def _compute_revision_count(self):
        for record in self:
            record.revision_count = self.env['certificate_planer.document_revision'].search_count([('document_id', '=', self.id)])

    def _compute_attachment_count(self):
        for record in self:
            record.attachment_count = self.env['ir.attachment'].search_count([('res_id', 'in', self.ids), ('res_model', '=', self._name)])

    # actions
    def view_document_report(self):
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/certificate_planer.document_report_view/%(document_id)s' % {'document_id': self.id},
        }
    
    def view_mdl_report(self):
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/certificate_planer.mdl_report_view/%(document_id)s' % {'document_id': self.id},
        }

    def store_tpi_report(self):
        self.ensure_one()

        # Remove existing report attachments
        self.env['ir.attachment'].search([
            ('name', 'in', [self.name + '.pdf', self.name.replace('MDL', 'TPI') + '.pdf']
        )]).unlink()

        # Render report
        pdf_content, content_type = self.env.ref('certificate_planer.mdl_report').render_qweb_pdf(self.id)
        pdf_content, content_type = self.env.ref('certificate_planer.tpi_report').render_qweb_pdf(self.id)
        # self.env['ir.attachment'].create({
        #     'name': self.name + '.pdf',
        #     'type': 'binary',
        #     'datas': base64.encodebytes(pdf_content),
        #     'res_model': self._name,
        #     'res_id': self.id
        # })

        # Return message
        message_id = self.env['certificate_planer.document.message'].create({'message': 'The reports have been generated. See attachments of this documents.'})
        return {
            'name': 'Message',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'certificate_planer.document.message',
            'res_id': message_id.id,
            'target': 'new'
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

class DocumentMessage(models.TransientModel):
    _name = 'certificate_planer.document.message'
    _description = "Show Message"

    message = fields.Text(required=True)

    def action_close(self):
        return {   
            'type': 'ir.actions.client',
            'tag': 'reload'
        }