from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)

class MDLReport(models.AbstractModel):
    _name = 'report.certificate_planer.mdl_report'
    _description = 'Certificate Planner MDL Report'

    def _get_report_values(self, docids, data=None):

        # Get the report and its context
        report = self.env['ir.actions.report']._get_report_from_name('certificate_planer.mdl_report')

        # Get the records selected for this report
        documents = self.env[report.model].browse(docids)

        # Get first document
        document = documents[0]

        # Get revisions and filter by change > status > shown on report attribute
        revisions = document.revision_ids.filtered(lambda r: r.change_id.status_id.show_on_report == True or not r.change_id)

        return {
            'docs': documents,
            'current_revision': document.current_revision_id,
            'revisions': revisions,
            'title_page_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.title_page_text'),
            'footer_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.footer_text')
        }