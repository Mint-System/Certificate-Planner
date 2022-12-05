from odoo import api, fields, models


class ChangeWizard(models.TransientModel):
    _name = 'certificate_planer.change.wizard'

    change_id = fields.Many2one('certificate_planer.change', default=lambda self: self.env.context.get('active_id', None))
    status_id = fields.Many2one('certificate_planer.change_status', default=lambda self: self.env['certificate_planer.change_status'].search([]))

    def set_status(self):

        self.change_id.write({
            'status_id': self.status_id.id
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'certificate_planer.change',
            'res_id': self.change_id.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
        }
