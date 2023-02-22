import itertools
from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime


class MCRReport(models.AbstractModel):
    _name = 'report.certificate_planer.mcr_report_view'
    _description = 'Certificate Planner MCR Report'

    def _get_survey_data(self, survey_result):
        survey_data = []
        input_ids = survey_result.user_input_line_ids
        for survey_input in survey_result.survey_id.question_and_page_ids:
            
            entry = {
                'type': 'question' if not survey_input.is_page else 'page',
                'text': survey_input.title,
                'options': '',
                'answert': '',
                'comment': '',
            }

            if not survey_input.is_page:
            
                # Process question options
                if survey_input.question_type == 'multiple_choice':
                    entry['options'] = [ {'id': suggestion.id, 'value': suggestion.value } for suggestion in survey_input.suggested_answer_ids]

                # Get answers
                answers = input_ids.filtered(lambda i: i.question_id == survey_input)

                # If multiple answers exist, then there is a comment
                if len(answers) > 1:
                    answer = answers.filtered(lambda a: a.answer_type in ['char_box', 'text_box'])[:1]
                    if answer:
                        entry['comment'] = answer.value_char_box or answer.value_text_box

                # Process answer of type sugestion
                answer = answers.filtered(lambda a: a.answer_type == 'suggestion')[:1]
                if answer:
                    entry['answer'] = answer.suggested_answer_id

            survey_data.append(entry)
        
        return survey_data

    def _get_report_values(self, docids, data=None):

        report_name = 'certificate_planer.mcr_report_view'

        # Get the report and its context
        report = self.env['ir.actions.report']._get_report_from_name(report_name)

        # Get the records selected for this report
        docs = self.env[report.model].browse(docids)

        # Get first document
        doc = docs[0]

        # Get the linked change
        change_id = docs.current_revision_id.change_id

        # Increase change version and update rpint date
        if data['report_type'] == 'pdf' or not doc.print_date:
            doc.sudo().print_date = datetime.now()
            change_id.version += 1

        return {
            'docids': docids, 
            'docs': docs,
            'print_date': docs.print_date,
            'dcc_survey_data': self._get_survey_data(change_id.dcc_survey_result_id),
            'occ_survey_data': self._get_survey_data(change_id.occ_survey_result_id),
            'conclusion_survey_data': self._get_survey_data(change_id.conclusion_survey_result_id),
        }