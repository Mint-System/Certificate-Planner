from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)

class DocumentReport(models.AbstractModel):
    _name = 'report.certificate_planer.document_report_view'
    _description = 'Certificate Planer Document Report'

    def _get_report_values(self, docids, data=None):

        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('certificate_planer.document_report_view')

        print("model", report.model)
        print("docids", docids)

        # get the records selected for this rendering of the report
        documents = self.env[report.model].browse(docids)

        # get most important records
        document = documents[0]
        certificate = document.certificate_id
        type = document.type_id
        revision = document.current_revision_id

        print("documents", documents[0].name)
        print('certificate.id', certificate.id)

        # get issues from certificate grouped by issue group
        issues_grouped = self.env['certificate_planer.issue'].read_group(
            [('certificate_id', '=', certificate.id)],
            fields=['id','name'],
            groupby=['group_id'])

        for groups in issues_grouped:
            for group in groups['group_id']:
                print("group", group)

        dis = {'key1':'value1','key2':'value2','key3':'value3','key4':'value4'}

        # issues
        issues=[]
        # issues.append({
        #     'name': 'issue1',
        #     'value': 'hello'
        # })
        # issues.append({
        #     'name': 'issue2',
        #     'value': 'world'
        # })
        issues.append(document)

        # return a custom rendering context
        return {
            'document': document,
            'certificate': certificate,
            'type': type,
            'revision': revision,
            'issues': issues,
            'dis': dis
        }   