from odoo import fields, models, api


class HrExpWizard(models.TransientModel):
    _name = 'update.experience.wizard'
    _description = 'Wizard cập nhật năm kinh nghiệm'

    # employee_ids = fields.Many2many('hr.employee', string="Employees")
    years_of_experience = fields.Integer("Số năm kinh nghiệm")

    def apply_experience_update(self):
        ids = self.env.context['active_ids']
        employees = self.env['hr.employee'].browse(ids)
        new_data={}
        if self.years_of_experience:
            new_data['years_of_experience'] = self.years_of_experience
        employees.write(new_data)