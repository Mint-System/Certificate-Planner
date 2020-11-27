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
        
        # process parts and docs
        for part in certificate.part_id:
            part_docs.append({
                'type': 'part',
                'part': part,
                'level': 0
            })

            # append doc level 0
            for doc in part.document_ids:
                part_docs.append({
                    'type:': 'doc',
                    'doc': doc
                })

            # refetch part
            part=self.env['certificate_planer.part'].browse(part.id)

            # iterate child part level 0
            for part in part.bom_id.part_ids:
                part_docs.append({
                    'type': 'part',
                    'part': part,
                    'level': 1
                })

                # append docs level 1
                for doc in part.document_ids:
                    part_docs.append({
                        'type:': 'doc',
                        'doc': doc
                    })

                # refetch part
                part=self.env['certificate_planer.part'].browse(part.id)

                # iterate child part level 1
                for part in part.bom_id.part_ids:
                    part_docs.append({
                        'type': 'part',
                        'part': part,
                        'level': 2
                    })

                    # append docs level 2
                    for doc in part.document_ids:
                        part_docs.append({
                            'type:': 'doc',
                            'doc': doc
                        })
                    
                    # refetch part
                    part=self.env['certificate_planer.part'].browse(part.id)

                    # iterate child part level 2
                    for part in part.bom_id.part_ids:
                        part_docs.append({
                            'type': 'part',
                            'part': part,
                            'level': 3
                        })

                        # append docs level 3
                        for doc in part.document_ids:
                            part_docs.append({
                                'type:': 'doc',
                                'doc': doc
                            })

        # return a custom rendering context
        return {
            'document': document,
            'certificate': certificate,
            'type': type,
            'revision': revision,
            'issue_groups': issue_groups,
            'log': log,
            'part_docs': part_docs
        }   