from lib2to3.pgen2.tokenize import group

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class UpdateSkillCert(models.TransientModel):
    _name = 'update.skill.cert'
    _description = 'Wizard chuyển chứng chỉ sang kỹ năng'

    check_department = fields.Boolean('Chọn bộ phận')
    department_id = fields.Many2one('hr.department', string='Bộ phận', default='')

    check_job = fields.Boolean('Chọn nghề')
    job_id = fields.Many2one('hr.job', string='Job Position', default='')

    check_experience = fields.Boolean('Chọn năm kinh nghiệm')
    min_experience = fields.Integer(string='Số năm kinh nghiệm ít nhất')

    add_certification = fields.Boolean(string='Thêm chứng chỉ', groups='hr_manager.group_manage_certification')
    cert_name = fields.Char('Tên chứng chỉ', groups='hr_manager.group_manage_certification')
    cert_date_obtained = fields.Date('Ngày nhận', groups='hr_manager.group_manage_certification')

    add_skill =fields.Boolean(string='Thêm kỹ năng', groups='hr_manager.group_manage_skill')
    skill_name = fields.Char('Tên kỹ năng', groups='hr_manager.group_manage_skill')
    eval = fields.Float('Đánh giá', groups='hr_manager.group_manage_skill')

    @api.onchange('check_department','check_job','min_experience')
    def _onchange_check_bool(self):
        for record in self:
            if not record.check_department:
                record.department_id = False
            if not record.check_job:
                record.job_id = False
            if not record.min_experience:
                record.min_experience = 0


    @api.constrains('cert_name','cert_date_obtained')
    def _check_cert(self):
        for record in self:
            if record.add_certification:
                if not record.cert_name:
                    raise ValidationError('Nhập tên')
                if not record.cert_date_obtained:
                    raise ValidationError('Phải nhập ngày nhận')

    @api.constrains('skill_name','skill_date_obtained')
    def _check_skill(self):
        for record in self:
            if record.add_skill:
                if not record.skill_name:
                    raise ValidationError('Nhập tên')


    def update_skill_cert_action(self):
        domain = []
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        if self.job_id:
            domain.append(('job_id', '=', self.job_id.id))
        if self.min_experience:
            domain.append(('years_of_experience', '>=', self.min_experience))

        ids = self.env.context['active_ids']
        employees = self.env['hr.employee'].search(domain) if domain  else self.env['hr.employee'].browse(ids)
        print(domain)
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
