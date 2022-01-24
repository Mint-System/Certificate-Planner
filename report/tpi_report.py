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

        # Get all documents and parts
        documents_and_parts = []
        documents_seen = []

        def get_documents_by_parts(part_ids):
            # Process each part
            for part in part_ids:
                # Get linked documents and process if not seen
                for document in part.document_ids:
                    # Append document if not seen
                    if document.id not in documents_seen and document.type_id.class_id.show_on_report:
                        documents_and_parts.append({
                            'doc': document,
                            'parts': document.part_ids
                        })
                        documents_seen.append(document.id)
                # Run this function for subparts
                get_documents_by_parts(
                    part.bom_id.part_ids.certificate_planer_part_id)
        get_documents_by_parts(document.certificate_id.part_id)
        # Group by document classes
        documents_by_class = {}
        for document_class in self.env['certificate_planer.document_class'].search([]):
            if document_class.show_on_report:
                documents_by_class[document_class.name] = {}
        for key, items in itertools.groupby(documents_and_parts, lambda r: r['doc'].type_id.class_id.name):
            new_items = list(items)
            # A key might be added multiple times
            if documents_by_class.get(key):
                items = documents_by_class[key]
                items = items + new_items
            else:
                items = new_items
            items = sorted(items, key=lambda r: r['doc'].name)
            items = sorted(items, key=lambda r: r['doc'].type_id.sequence)
            documents_by_class[key] = items
        # Remove keys without docs
        documents_by_class = dict(
            filter(lambda r: r[1], documents_by_class.items()))

        # Replace placholders
        tpi_page_text = self.env['ir.config_parameter'].sudo().get_param('certificate_planer.tpi_page_text')
        tpi_page_text = tpi_page_text.replace('DOCUMENT_NAME', document.name).replace('DOCUMENT_REVISION_TITLE', document.current_revision_id.index_id.name)

        return {
            'docs': documents,
            'current_revision': document.current_revision_id,
            'print_date': document.print_date,
            'documents_by_class': documents_by_class,
            'tpi_page_text': tpi_page_text,
            'title_page_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.title_page_text'),
            'footer_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.footer_text'),
            'design_organisation_statement_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.design_organisation_statement_text')
        }
