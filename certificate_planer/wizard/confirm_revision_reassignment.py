from odoo import models, fields, api

class ConfirmRevisionReassignment(models.TransientModel):
    _name = 'certificate_planer.confirm.revision.reassignment'
    _description = 'Confirm Revision Reassignment'

    revision_id = fields.Many2one('certificate_planer.document_revision')
    new_change_id = fields.Many2one('certificate_planer.change')

    def action_confirm(self):
        self.revision_id.change_id = self.new_change_id.id
        return {'type': 'ir.actions.act_window_close'}
