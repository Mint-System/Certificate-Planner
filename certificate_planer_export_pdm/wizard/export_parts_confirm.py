import logging
from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class ExportPartsConfirm(models.TransientModel):
    _name = 'certificate_planer.exports_parts_confirm'
    _description = 'Confirm Parts Export to PDM'

    confirm_text = fields.Char(readonly=True)
    part_count = fields.Integer(readonly=True)

    def default_get(self, fields_list):
        _logger.warning("default_get")
        result = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        part_count = len(active_ids)
        result['part_count'] = part_count
        result['confirm_text'] = _("Export %(count)s selected part(s) to PDM?") % {
            'count': part_count,
        }

        return result

    def action_confirm_export_parts(self):
        _logger.warning("action_confirm_export_parts")
        active_ids = self.env.context.get('active_ids', [])
        # self.env['certificate_planer.part']._action_export_all_xml()
        parts = self.env['certificate_planer.part'].browse(active_ids).exists()
        if parts:
            parts._action_export_all_xml()

        return {'type': 'ir.actions.act_window_close'}
