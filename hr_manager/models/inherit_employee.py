from odoo import fields, models, api


class InheritEmployee(models.Model):
    _inherit = 'hr.employee'

    years_of_experience = fields.Integer('Năm kinh nghiệm', compute='_compute_years_of_experience', store=True)
    certification_ids = fields.One2many('employee.certifications', 'employee_id', string='Chứng chỉ')
    skill_ids = fields.One2many('employee.skills', 'employee_id', string='Kỹ năng')

    @api.depends('certification_ids', 'skill_ids')
    def _compute_years_of_experience(self):
        for record in self:
            year = []
            for certification in record.certification_ids:
                if certification.date_obtained:
                    year.append(certification.date_obtained.year)
            yoe = min(year) if year else 0
            if year:
                record.years_of_experience = fields.Date.today().year - yoe
            else:
                record.years_of_experience = 0


            print(year)
