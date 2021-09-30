from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)
import itertools

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

        # Get changes from document > certificate
        changes = document.certificate_id.change_ids
        # Filter changes with status show on report
        changes = changes.filtered(lambda r: r.status_id.show_on_report == True)
        # Sort changes by change_id_id.sequence
        changes = changes.sorted(key=lambda r: r.change_id_id.sequence)

        # Get documents by change
        change_revisions = {}
        for change in changes:
            change_revisions[change.id] = {}
            # Group document revisions by document > document type > document class
            for key, items in itertools.groupby(change.revision_ids, lambda r: r.document_id.type_id.class_id.name):
                items = list(items)
                # Sort revisions by type_id.sequence and document_id.name
                if items:
                    items = sorted(items, key=lambda r: r.document_id.name)
                    items = sorted(items, key=lambda r: r.document_id.type_id.sequence)
                change_revisions[change.id][key] = {}
                change_revisions[change.id][key]['items'] = items
                change_revisions[change.id][key]['class'] = items[0].document_id.type_id.class_id or False

            _logger.info(change_revisions[change.id])

        # Get all parts for certificate
        # parts=[]
        # def get_subparts(level, part_ids):
        #     if (level < 5):
        #         for part in part_ids:
        #             parts.append({
        #                 'part': part,
        #                 'level': level
        #             })
        #             part=self.env['certificate_planer.part'].browse(part.id)
        #             # Call function for subparts
        #             get_subparts(level+1, part.bom_id.part_ids.certificate_planer_part_id)
        # get_subparts(0, document.certificate_id.part_id)

        return {
            'docs': documents,
            'current_revision': document.current_revision_id,
            'revisions': revisions,
            'changes': changes,
            'change_revisions': change_revisions,
            'parts'
            'title_page_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.title_page_text'),
            'footer_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.footer_text')
        }