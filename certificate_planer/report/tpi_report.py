import itertools
from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)
from . import mdl_data

class TPIReport(models.AbstractModel):
    _name = 'report.certificate_planer.tpi_report_view'
    _description = 'Certificate Planner TPI Report'

    def _get_report_values(self, docids, data=None):
        report_name = 'certificate_planer.tpi_report_view'
        return mdl_data._get_report_values(self, docids, data, report_name)