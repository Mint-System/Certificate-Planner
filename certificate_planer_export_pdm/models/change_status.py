from odoo import fields, models


class ChangeStatus(models.Model):
    _inherit = "certificate_planer.change_status"

    pdm_export_trigger = fields.Boolean(default=False)
