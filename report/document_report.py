from odoo import api, models

# class ParticularReport(models.AbstractModel):
#     _name = 'report.certificate_planer.document_report'
#     _description = 'report.certificate_planer.document_report'

#     def _get_report_values(self, docids, data=None):

#         # get the report action back as we will need its data
#         report = self.env['ir.actions.report']._get_report_from_name('certificate_planer.document_repor')
        
#         # get the records selected for this rendering of the report
#         obj = self.env[report.model].browse(docids)
        
#         # return a custom rendering context
#         return {
#             'lines': docids.get_lines()
#         }