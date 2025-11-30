from odoo import models, fields


class ChangeStatus(models.Model):
    _inherit = 'certificate_planer.change_status'
  
    pdm_export_trigger = fields.Boolean(default=False)