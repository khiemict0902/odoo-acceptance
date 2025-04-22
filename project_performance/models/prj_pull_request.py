from odoo import api, fields, models
from odoo.exceptions import UserError


class PullRequest(models.Model):
    _name = 'prj.pull.request'
    _description = 'Pull Request của dự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [('pr_unique_name','UNIQUE(name)','Tên bản ghi đã tồn tại'),
                        ('pr_unique_linkpr','UNIQUE(link_pr)','Link Pull request đã tồn tại')]


    name = fields.Char('Tên', required=True, tracking=True)
    description = fields.Text('Mô tả')
    tags_ids = fields.Many2many('project.tags', string='Thẻ tags')
    link_pr = fields.Char('Link pull request', help="Link phải có dạng 'https://_/pull/_id'", tracking=True)
    id_pr = fields.Char('ID Pull Request', compute='_compute_id_pr', store=True)
    state = fields.Selection([('samdev', 'Samdev'),
                              ('uat', 'UAT'),
                              ('staging', 'Staging'),
                              ('product', 'Production')
                              ], 'Trạng thái', default='samdev', tracking=True)
    person_create_id = fields.Many2one('res.users', string='Người tạo', default=lambda self: self.env.user)
    date_create = fields.Date(string='Ngày tạo', default=fields.Date.today)
    task_id = fields.Many2one('project.task', 'Nhiệm vụ')

    @api.depends('link_pr')
    def _compute_id_pr(self):
        for pull in self:
            if pull.link_pr and "pull/" in pull.link_pr:
                pull.id_pr = pull.link_pr.split('/')[-1]
            else:
                pull.id_pr = False

    def action_uat(self):
        for rec in self:
            if not rec.id_pr:
                raise UserError('Yêu cầu phải có Link Pull Request hợp lệ để chuyển sang UAT')
            rec.state = 'uat'

    def action_rollback2samdev(self):
        for rec in self:
            rec.state = 'samdev'

    def action_rollback2uat(self):
        for rec in self:
            rec.state = 'uat'

    def action_rollback2staging(self):
        for rec in self:
            rec.state = 'staging'