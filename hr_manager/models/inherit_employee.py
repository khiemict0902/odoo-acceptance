from odoo import fields, models, api


class InheritEmployee(models.Model):
    _inherit = 'hr.employee'

    years_of_experience = fields.Integer('Năm kinh nghiệm', compute='_compute_years_of_experience', store=True)
    certification_ids = fields.One2many('employee.certifications', 'employee_id', string='Chứng chỉ')
    skill_ids = fields.One2many('employee.skills', 'employee_id', string='Kỹ năng')

    @api.depends('certification_ids')
    def _compute_years_of_experience(self):
        for record in self:
            years = record.certification_ids.mapped('date_obtained')
            years = [d.year for d in years if d]
            if years:
                record.years_of_experience = fields.Date.today().year - min(years)

            else:
                record.years_of_experience = 0


            print(years)
