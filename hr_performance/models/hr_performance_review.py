from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class HrPerformanceReview(models.Model):
    _name = 'hr.performance.review'
    _description = 'Lưu trữ thông tin đánh giá hiệu suất của nhân viên.'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên bản ghi', required=True)
    review_date = fields.Date('Ngày đánh giá')
    performance_score = fields.Selection([
        ('1','Poor'),
        ('2', 'Average'),
        ('3', 'Good'),
        ('4', 'Excellent'),
    ],'Điểm đánh giá hiệu suất', required=True)
    comment = fields.Text('Bình luận về đánh giá')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
    ], 'Trạng thái', required=True, tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Nhân viên', required=True)
    reviewer_id = fields.Many2one('res.users', string='Người đánh giá')

    @api.constrains('review_date')
    def _check_review_date(self):
        for record in self:
            if record.review_date < fields.Date.today():
                raise ValidationError('Ngày đánh giá không được trước ngày hôm nay')


    def write(self, vals):
        for record in self:
            if record.state != 'draft':
                if self.env.user.has_group('hr_performance.group_hr_review_employee'):
                    raise UserError("Chỉ bản ghi ở trạng thái 'Draft' mới được chỉnh sửa.")
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
