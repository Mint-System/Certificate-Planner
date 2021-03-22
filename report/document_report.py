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

        # get first document
        document = documents[0]

        # get issues from certificate grouped by issue group
        issues_grouped = self.env['certificate_planer.issue'].read_group(
            [('certificate_id', '=', document.certificate_id.id)],
            fields=['id'],
            groupby=['group_id'])

        # dict log of ammendments
        log={}

        # issue groups
        issue_groups=[]

        # process issue group results
        for group in issues_grouped:
            issue_group_id=group['group_id'][0]
            issue_domain=group['__domain']
    
            # get issue group
            issue_group=self.env['certificate_planer.issue_group'].browse(issue_group_id)
            issue_groups.append(issue_group)

            # create key in log
            log[issue_group.id]={'issues': [] }

            # get issues from domain filter
            issues=self.env['certificate_planer.issue'].search(issue_domain)
            log[issue_group.id]['issues']=issues

        # parts and docs
        part_docs=[]
        #doc_seen=[]

        # function to process
        def append_part_docs(level,part_ids):

            # prevent loop
            if (level < 5):
                for part in part_ids:
                    part_docs.append({
                        'type': 'part',
                        'part': part,
                        'level': level
                    })

                    for doc in part.document_ids:
                        #if doc.id not in doc_seen:
                            part_docs.append({
                                'type:': 'doc',
                                'doc': doc
                            })
                            #doc_seen.append(doc.id)
                    
                    # refetch part
                    part=self.env['certificate_planer.part'].browse(part.id)

                    # run this function for child part
                    append_part_docs(level+1, part.bom_id.part_ids)
        
        # process parts and docs
        append_part_docs(0, document.certificate_id.part_id)

        # return a custom rendering context
        return {
            'docs': documents,
            'revision': document.current_revision_id,
            'issue_groups': issue_groups,
            'log': log,
            'part_docs': part_docs
        }   