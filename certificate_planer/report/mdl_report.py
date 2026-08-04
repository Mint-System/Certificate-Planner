import logging

from odoo import models

_logger = logging.getLogger(__name__)
from . import mdl_data


class MDLReport(models.AbstractModel):
    _name = "report.certificate_planer.mdl_report_view"
    _description = "Certificate Planner MDL Report"

    def _get_report_values(self, docids, data=None):
        report_name = "certificate_planer.mdl_report_view"
        return mdl_data._get_report_values(self, docids, data, report_name)
