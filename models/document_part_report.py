from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentPartReport(models.Model):
    _name = 'certificate_planer.document_part_report'
    _description = 'Certificate Planner Document Part Report'
    _auto = False # Disable the database table automatic creation

    # fields
    document = fields.Many2one('certificate_planer.document')
    part = fields.Many2one('certificate_planer.part')
    
    # defaults
    def init(self):
        self._cr.execute(""" 
            CREATE OR REPLACE VIEW certificate_planer_document_part_report AS ( 
            SELECT row_number() OVER () as id,
            cpd.id AS document,
            cpp.id AS part
            FROM certificate_planer_document cpd
            LEFT JOIN certificate_planer_document_certificate_planer_part_rel cpdcpp ON cpd.id = cpdcpp.certificate_planer_document_id 
            LEFT JOIN certificate_planer_part cpp ON cpdcpp.certificate_planer_part_id = cpp.id)
        """)