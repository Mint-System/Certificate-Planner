import itertools
from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime


class MCRReport(models.AbstractModel):
    _name = 'report.certificate_planer.mcr_report_view'
    _description = 'Certificate Planner MCR Report'

    def _get_report_values(self, docids, data=None):

        report_name = 'certificate_planer.mcr_report_view'

        # Get the report and its context
        report = self.env['ir.actions.report']._get_report_from_name(report_name)

        # Get the records selected for this report
        docs = self.env[report.model].browse(docids)

        # Get first document
        doc = docs[0]

        # Increase change version and update rpint date
        if data['report_type'] == 'pdf' or not doc.print_date:
            doc.sudo().print_date = datetime.now()
            docs.current_revision_id.change_id.version += 1

        return {
            'docids': docids, 
            'docs': docs,
            'print_date': docs.print_date,
        }