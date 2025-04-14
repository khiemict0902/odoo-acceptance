from odoo import fields, models, api
from odoo.exceptions import ValidationError

class InheritApplicants(models.Model):
    _inherit = 'hr.applicant'

    detailed_status_id = fields.Many2one('details.state', 'Trạng thái chi tiết')
    graduated_school = fields.Char('Trường tốt nghiệp')
    gpa_4_scale = fields.Float('GPA thang 4', compute='_compute_gpa_4_scale')
    gpa_10_scale = fields.Float('GPA thang 10')

    @api.constrains('gpa_10_scale')
    def _check_gpa_10_scale(self):
        for record in self:
            if record.gpa_10_scale > 10 or record.gpa_10_scale < 0:
                raise ValidationError('Giá trị vượt quá 10 hoặc giá trị bị âm')

    @api.depends('gpa_10_scale', 'gpa_4_scale')
    def _compute_gpa_4_scale(self):
        for record in self:
            record.gpa_4_scale = record.gpa_10_scale / 2.5

    def accept_action(self):
        for record in self:
            record.interviewer_ids = self.env.user