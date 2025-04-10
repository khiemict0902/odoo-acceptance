from odoo import fields, models, api
from odoo.exceptions import UserError


class EmployeeExp(models.Model):
    _inherit = 'hr.employee'

    years_of_experience = fields.Integer("Số năm kinh nghiệm", groups='hr_exp.group_hr_experience_manager')

    @api.model
    def create(self, vals):
        if vals.get('years_of_experience') > 30:
            raise UserError('Số năm kinh nghiệm tối đa là 30')
        if vals.get('years_of_experience') < 0:
            raise UserError('Số năm kinh nghiệm không được âm')
        return super().create(vals)

    def write(self, vals):
        if vals.get('years_of_experience') > 30:
            raise UserError('Số năm kinh nghiệm tối đa là 30')
        if vals.get('years_of_experience') < 0:
            raise UserError('Số năm kinh nghiệm không được âm')

        return super().write(vals)