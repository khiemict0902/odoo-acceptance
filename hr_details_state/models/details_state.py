from odoo import fields, models, api


class DetailsState(models.Model):
    _name = 'details.state'
    _description = 'Quản lý thông tin chi tiết về trạng thái của ứng viên. '
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Tên đã tồn tại')
    ]

    name = fields.Char('Tên', required=True)
    description = fields.Text('Mô tả chi tiết')
    applicants_ids = fields.One2many('hr.applicant', 'detailed_status_id','Ứng viên')
