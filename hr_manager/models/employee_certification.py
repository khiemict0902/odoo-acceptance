from odoo import fields, models, api
from odoo.exceptions import UserError


class EmployeeCertification(models.Model):
    _name = 'employee.certifications'
    _description = 'Quản lý chứng chỉ nhân viên'

    name = fields.Char('Tên chứng chỉ',required=True)
    date_obtained = fields.Date('Ngày nhận')
    employee_id = fields.Many2one('hr.employee', string='Nhân viên')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._apply_certificate_effect()
        cert_name =vals.get('name','')
        employee_id = vals.get('employee_id','')

        print(cert_name)
        if 'Chứng chỉ' in cert_name[0:10]:
            skill_add = "Kỹ năng " + cert_name[10:]

            existing_skill = self.env['employee.skills'].search([
                ('name', '=', skill_add),
                ('employee_id', '=', employee_id)
            ], limit=1)

            if not existing_skill:
                self.env['employee.skills'].create({
                    'name': skill_add,
                    'employee_id': employee_id
                })
        else:
            raise UserError("Chứng chỉ không hợp lệ. Tên phải có chữ 'Chứng chỉ' ở đầu. VD: Chứng chỉ Tin học")

        return res

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            rec._apply_certificate_effect()
            cert_name = rec.name
            employee_id = rec.employee_id.id

            if 'Chứng chỉ' in cert_name[0:10]:
                skill_add = "Kỹ năng " + cert_name[10:]

                existing_skill = self.env['employee.skills'].search([
                    ('name', '=', skill_add),
                    ('employee_id', '=', employee_id)
                ], limit=1)

                if not existing_skill:
                    self.env['employee.skills'].create({
                        'name': "Kỹ năng " + cert_name[10:],
                        'employee_id': self.employee_id.id
                    })
            else:
                raise UserError("Chứng chỉ không hợp lệ. Tên phải có chữ 'Chứng chỉ' ở đầu. VD: Chứng chỉ Tin học")

        return res

    def _apply_certificate_effect(self):
        for rec in self:
            emp = rec.employee_id
            if len(emp.skill_ids) > 10:
                raise UserError("Nhân viên không được có quá 10 kỹ năng. Hành động bị huỷ.")

