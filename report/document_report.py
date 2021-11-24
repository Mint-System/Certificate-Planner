from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)


class DocumentReport(models.AbstractModel):
    _name = 'report.certificate_planer.document_report_view'
    _description = 'Certificate Planner Document Report'

    def _get_report_values(self, docids, data=None):

        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name(
            'certificate_planer.document_report_view')

        # get the records selected for this rendering of the report
        documents = self.env[report.model].browse(docids)

        # get first document
        document = documents[0]

        # get changes from certificate grouped by change id
        changes_grouped = self.env['certificate_planer.change'].read_group(
            [('certificate_id', '=', document.certificate_id.id)],
            fields=['id'],
            groupby=['change_id_id'])

        # dict log of ammendments
        log = {}

        # change id
        change_ids = []

        # process change grouped records
        for group in changes_grouped:
            change_id_id = group['change_id_id'][0]
            change_domain = group['__domain']

            # get change group
            change_id = self.env['certificate_planer.change_id'].browse(
                change_id_id)
            change_ids.append(change_id)

            # create key in log
            log[change_id.id] = {'changes': []}

            # get changes from grouped domain filter
            changes = self.env['certificate_planer.change'].search(
                change_domain)
            log[change_id.id]['changes'] = changes

        # parts and docs
        part_docs = []
        # doc_seen=[]

        # function to process
        def append_part_docs(level, part_ids):

            # prevent loop
            if (level < 5):
                for part in part_ids:

                    part_docs.append({
                        'type': 'part',
                        'part': part,
                        'level': level
                    })

                    for doc in part.document_ids:
                        # if doc.id not in doc_seen:
                        part_docs.append({
                            'type:': 'doc',
                            'doc': doc
                        })
                        # doc_seen.append(doc.id)

                    # refetch part
                    part = self.env['certificate_planer.part'].browse(part.id)

                    # run this function for child part
                    append_part_docs(
                        level+1, part.bom_id.part_ids.certificate_planer_part_id)

        # process parts and docs
        append_part_docs(0, document.certificate_id.part_id)

        # return a custom rendering context
        return {
            'docs': documents,
            'revision': document.current_revision_id,
            'change_ids': change_ids,
            'log': log,
            'part_docs': part_docs,
            'title_page_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.title_page_text'),
            'footer_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.footer_text'),
            'design_organisation_statement_text': self.env['ir.config_parameter'].sudo().get_param('certificate_planer.design_organisation_statement_text')
        }
