from odoo import fields, models, api


class EmployeeSkills(models.Model):
    _name = 'employee.skills'
    _description = 'Quản lý đánh giá kỹ năng nhân viên'

    name = fields.Char('Tên kỹ năng', required=True)
    eval = fields.Float('Đánh giá')
    employee_id = fields.Many2one('hr.employee', string='Nhân viên')

