from odoo import fields, models, api
from odoo.exceptions import UserError


class CertificationToSkillWizard(models.TransientModel):
    _name = 'certification.to.skill.wizard'
    _description = 'Wizard chọn chứng chỉ và chuyển thành kỹ năng'

    certification_ids = fields.Many2many(
        'employee.certifications',
        string="Chứng chỉ",
        domain="[('employee_id', '=', employee_id)]"
    )

    employee_id = fields.Many2one('hr.employee', string="Nhân viên")


    def action_convert_cert_to_skills(self):
        for cert in self.certification_ids:
            if 'Chứng chỉ' in cert.name[0:10]:
                self.env['employee.skills'].create({
                    'name': "Kỹ năng " + cert.name[10:],
                    'employee_id': self.employee_id.id
                })
            else:
                raise UserError("Chứng chỉ không hợp lệ. Tên phải có chữ 'Chứng chỉ' ở đầu. VD: Chứng chỉ Tin học")
