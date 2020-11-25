from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)

class DocumentReport(models.AbstractModel):
    _name = 'report.certificate_planer.document_report_view'
    _description = 'Certificate Planer Document Report'

    def _get_report_values(self, docids, data=None):

        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('certificate_planer.document_report_view')

        # get the records selected for this rendering of the report
        documents = self.env[report.model].browse(docids)

        # get most important records
        document = documents[0]
        certificate = document.certificate_id
        type = document.type_id
        revision = document.current_revision_id

        # get issues from certificate grouped by issue group
        issues_grouped = self.env['certificate_planer.issue'].read_group(
            [('certificate_id', '=', certificate.id)],
            fields=['id','name'],
            groupby=['group_id'])

        # dict log of ammendments
        log={}

        # test
        #issues=[]

        # issue groups
        issue_groups=[]

        for group in issues_grouped:
            issue_group_id=group['group_id'][0]
            issue_domain=group['__domain']
            print("id", issue_group_id)
            print("name", group['group_id'][1])
            print("domain", issue_domain)
    
            # get issue group
            issue_group=self.env['certificate_planer.issue_group'].browse(issue_group_id)
            print("issue_group.name", issue_group.name)
            issue_groups.append(issue_group)

            # create key in log
            log[issue_group.id]={'documents': [], 'issues': [] }

            # get issues from domain filter
            issues=self.env['certificate_planer.issue'].search(issue_domain)
            print("issues",issues)
            log[issue_group.id]['issues']=issues

            # get issues from domain filter
            #issue=self.env['certificate_planer.issue'].browse(issue_group_id)
            #print("name", issue.name)
            #issues.append(issue)

            # log[issue.id] = {'revisions': [], 'orderpoint': []}


        #dis = {'key1':'value1','key2':'value2','key3':'value3','key4':'value4'}
        
        # issues
        #issues=[]
        # issues.append({
        #     'name': 'issue1',
        #     'value': 'hello'
        # })
        # issues.append({
        #     'name': 'issue2',
        #     'value': 'world'
        # })
        #issues.append(document)

        # return a custom rendering context
        return {
            'document': document,
            'certificate': certificate,
            'type': type,
            'revision': revision,
            #'issues': issues,
            'issue_groups': issue_groups,
            'log': log
            # 'dis': dis
        }   