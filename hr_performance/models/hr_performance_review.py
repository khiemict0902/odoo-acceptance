from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class HrPerformanceReview(models.Model):
    _name = 'hr.performance.review'
    _description = 'Lưu trữ thông tin đánh giá hiệu suất của nhân viên.'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [('unique_name','UNIQUE(name)','Tên bản ghi ton tai')]

    name = fields.Char('Tên', required=True)
    review_date = fields.Date('Ngày đánh giá')
    performance_score = fields.Selection([
        ('1','Kém'),
        ('2', 'Trung bình'),
        ('3', 'Tốt'),
        ('4', 'Xuất sắc'),
    ],'Điểm đánh giá hiệu suất', required=True)
    comment = fields.Text('Bình luận về đánh giá')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('submitted', 'Đã Nộp'),
        ('approved', 'Chấp nhận'),
    ], 'Trạng thái', required=True, default='draft', tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True)
    reviewer_id = fields.Many2one('res.users', string='Người đánh giá')

    @api.constrains('review_date')
    def _check_review_date(self):
        for record in self:
            if record.review_date and record.review_date < fields.Date.today():
                raise ValidationError('Ngày đánh giá không được trước ngày hôm nay')

            if record.review_date and record.review_date < record.create_date.date():
                raise ValidationError('Ngày đánh giá không được trước ngày tạo bản ghi')


    def write(self, vals):
        for record in self:
            if record.state != 'draft':
                if self.env.context.get('install_mode'):
                    return super().write(vals)
                
                if not self.env.user.has_group('hr_performance.group_hr_review_manager'):
                    raise UserError("Chỉ bản ghi ở trạng thái 'Draft' nhân viên mới được chỉnh sửa.")
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                if not self.env.user.has_group('hr_performance.group_hr_review_admin'):
                    raise UserError("Chỉ Admin mới được xóa.")
        return super().unlink()

    def submit_action(self):
        for record in self:
            record.state = 'submitted'

    def approve_action(self):
        for record in self:
            record.state = 'approved'

    def draft_action(self):
        for record in self:
            record.state = 'draft'
