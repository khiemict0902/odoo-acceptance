from lib2to3.pgen2.tokenize import group

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class UpdateSkillCert(models.TransientModel):
    _name = 'update.skill.cert'
    _description = 'Wizard chuyển chứng chỉ sang kỹ năng'



    add_certification = fields.Boolean(string='Thêm chứng chỉ', groups='hr_manager.group_manage_certification')
    cert_name = fields.Char('Tên chứng chỉ', groups='hr_manager.group_manage_certification')
    cert_date_obtained = fields.Date('Ngày nhận', groups='hr_manager.group_manage_certification')

    add_skill =fields.Boolean(string='Thêm kỹ năng', groups='hr_manager.group_manage_skill')
    skill_name = fields.Char('Tên kỹ năng', groups='hr_manager.group_manage_skill')
    eval = fields.Float('Đánh giá', groups='hr_manager.group_manage_skill')



    def update_skill_cert_action(self):
        ids = self.env.context['active_ids']

        employees = self.env['hr.employee'].browse(ids)

        for emp in employees:
            if self.add_certification and self.cert_name:
                self.env['employee.certifications'].create({
                    'name': self.cert_name,
                    'date_obtained': self.cert_date_obtained,
                    'employee_id': emp.id
                })

            if self.add_skill and self.skill_name:
                existing = emp.skill_ids.filtered(lambda s: s.name == self.skill_name)
                if existing:
                    existing.write({'level': self.eval})
                else:
                    self.env['employee.skills'].create({
                        'name': self.skill_name,
                        'eval': self.eval,
                        'employee_id': emp.id
                    })
