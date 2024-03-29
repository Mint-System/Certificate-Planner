from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class Change(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'certificate_planer.change'
    _description = 'Certificate Planner Change'
    _rec_name = 'change_id_id'

    project_title = fields.Char(required=True)
    description = fields.Text()
    certificate_id = fields.Many2one("certificate_planer.certificate", string="Certificate", tracking=True)
    aircraft_type_id = fields.Many2one("certificate_planer.aircraft_type", string="Aircraft Type", tracking=True, ondelete="restrict")
    authority_reference = fields.Char()
    reference = fields.Char(string="Aerolite Reference")
    part_count = fields.Integer(compute='_compute_part_count')
    revision_count = fields.Integer(compute='_compute_revision_count')
    item_count = fields.Integer(compute='_compute_item_count')
    version = fields.Integer(readonly=True)
    target_approval_date = fields.Date()
    approval_date = fields.Date()
    references = fields.Text()

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    dcc_survey_template_id = fields.Many2one('survey.survey', related='company_id.dcc_survey_template_id')
    occ_survey_template_id = fields.Many2one('survey.survey', related='company_id.occ_survey_template_id')
    conclusion_survey_template_id = fields.Many2one('survey.survey', related='company_id.conclusion_survey_template_id')

    dcc_survey_result_id = fields.Many2one('survey.user_input')
    occ_survey_result_id = fields.Many2one('survey.user_input')
    conclusion_survey_result_id = fields.Many2one('survey.user_input')

    status_id = fields.Many2one("certificate_planer.change_status", tracking=True, default=lambda self: self.env['certificate_planer.change_status'].search([]), ondelete="restrict")
    classification_id = fields.Many2one("certificate_planer.change_classification", tracking=True, ondelete="restrict")
    change_id_id = fields.Many2one("certificate_planer.change_id", required=True, string="Change ID", tracking=True, ondelete="restrict")
    
    part_ids = fields.Many2many("certificate_planer.part", string="Parts", ondelete="restrict")

    revision_ids = fields.One2many("certificate_planer.document_revision", "change_id", string="Document Revisions")
    item_ids = fields.One2many("certificate_planer.post_certification_item", "change_id", string="Post Certification Items")

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('%s (%s)') % (rec.change_id_id.name, rec.certificate_id.part_id.name)))
        return res

    def unlink(self):
        if not self.env.user.has_group('certificate_planer.group_certificate_planer_administrator') and len(self) > 1:
            raise UserError(_('You cannot delete multiple documents.'))
        return super().unlink()

    def _compute_part_count(self):
        for record in self:
            record.part_count = len(self.part_ids)
    
    def _compute_revision_count(self):
        for record in self:
            record.revision_count = len(self.revision_ids)

    def _compute_item_count(self):
        for record in self:
            record.item_count = len(self.item_ids)

    def view_part_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Parts",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.part",
            "domain": [("id", "in", [t.id for t in self.part_ids])],
            "context": "{'create': False}",
        }

    def view_revision_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Document Revisions",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.document_revision",
            "domain": [("change_id", "=", self.id)],
            "context": "{'create': False}",
        }

    def view_item_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Post Certification Items",
            "view_mode": "tree,form",
            "res_model": "certificate_planer.post_certification_item",
            "domain": [("change_id", "=", self.id)],
            "context": "{'create': False}",
        }

    def action_start_survey(self, template_id):
        self.ensure_one()
        answer = template_id.sudo()._create_answer(user=self.env.user, partner=self.env.user.partner_id)
        answer.write({
            'change_id': self.id,
            'version': 1,
        })
        res = template_id.action_start_survey(answer)
        res['target'] = 'new'
        return res

    def action_revise_result(self, template_id, result_id):
        self.ensure_one()
        answer = template_id.sudo()._create_answer(user=self.env.user, partner=self.env.user.partner_id)
        answer.write({
            'change_id': self.id,
            'version': result_id.version + 1,
        })
        res = template_id.action_start_survey(answer)
        res['target'] = 'new'
        return res

    def action_start_dcc_survey(self):
        return self.action_start_survey(self.dcc_survey_template_id)

    def action_revise_dcc_result(self):
        return self.action_revise_result(self.dcc_survey_template_id, self.dcc_survey_result_id)

    def action_start_occ_survey(self):
        return self.action_start_survey(self.occ_survey_template_id)

    def action_revise_occ_result(self):
        return self.action_revise_result(self.occ_survey_template_id, self.occ_survey_result_id)

    def action_start_conclusion_survey(self):
        return self.action_start_survey(self.conclusion_survey_template_id)

    def action_revise_conclusion_result(self):
        return self.action_revise_result(self.conclusion_survey_template_id, self.conclusion_survey_result_id)

    def action_reload(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }