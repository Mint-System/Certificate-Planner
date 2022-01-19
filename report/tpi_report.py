import itertools
from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)


class TPIReport(models.AbstractModel):
    _name = 'report.certificate_planer.tpi_report_view'
    _description = 'Certificate Planner TPI Report'

    def _get_report_values(self, docids, data=None):

        # Get the report and its context
        report = self.env['ir.actions.report']._get_report_from_name(
            'certificate_planer.tpi_report_view')

        # Get the records selected for this report
        documents = self.env[report.model].browse(docids)

        # Get first document
        document = documents[0]

        return {
            'docs': documents,
            'current_revision': document.current_revision_id,
            'tpi_page_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.tpi_page_text'),
            'title_page_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.title_page_text'),
            'footer_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.footer_text'),
            'design_organisation_statement_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.design_organisation_statement_text')
        }
