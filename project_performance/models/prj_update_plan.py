from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import UserError


class UpdatePlan(models.Model):
    _name = 'prj.update.plan'
    _description = 'Bản kế hoạch cập nhật sự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [('plan_unique_name','UNIQUE(name)','Tên bản ghi đã tồn tại')]

    name = fields.Char('Tên', required=True, tracking=True)
    description = fields.Html('Mô tả')
    state = fields.Selection([('draft', 'Draft'),
                              ('pending', 'Pending'),
                              ('approved', 'Approved'),
                              ('done', 'Done'),
                              ('closed', 'Closed')],
                             string='Trạng thái', default='draft', tracking=True)
    date_create = fields.Date(string='Ngày tạo', default=fields.Date.today)

    project_id = fields.Many2one('project.project', string='Dự án')
    task_ids =fields.Many2many('project.task', string='Nhiệm vụ')
    task_domain = fields.Json('Domain', compute='_compute_task_domain')

    pr_ids = fields.Many2many('prj.pull.request', string='Pull Requests', compute='_compute_pr_ids', stored=True)

    count_task = fields.Integer(compute='_compute_count_task')
    count_pr = fields.Integer(compute='_compute_count_pr')

    @api.depends('task_ids')
    def _compute_pr_ids(self):
        for record in self:
            record.pr_ids = record.task_ids.mapped('pr_ids')

    @api.depends('task_ids')
    def _compute_count_task(self):
        for record in self:
            record.count_task = len(record.mapped('task_ids'))

    @api.depends('pr_ids')
    def _compute_count_pr(self):
        for record in self:
            record.count_pr = len(record.mapped('pr_ids'))

    @api.depends('project_id')
    def _compute_task_domain(self):
        for record in self:
            if record.project_id:
                record.task_domain = [('project_id', '=', record.project_id.id),('is_update', '=', False)]
            else:
                record.task_domain = [('is_update', '=', False)]

    def done_action(self):
        for record in self:
            state_list = record.pr_ids.mapped('state')
            if not all(p=='uat' for p in state_list):
                raise UserError('Tất cả trạng thái của Pull Request là UAT mới có thể hoàn thành')
            record.state = 'done'
            record.task_ids.write({'is_update': True})
            record.pr_ids.write({'state': 'staging'})

    def close_action(self):
        for record in self:
            record.state = 'closed'
            record.pr_ids.write({'state': 'product'})

    def pending_action(self):
        for record in self:
            if not record.task_ids:
                raise UserError('Phải có nhiệm vụ để chờ duyệt')
            record.state = 'pending'


    def approve_action(self):
        for record in self:
            if not record.pr_ids:
                raise UserError('Phải có pull request để duyệt')
            record.state = 'approved'

    def action_rollback2done(self):
        for record in self:
            record.state = 'done'
            record.pr_ids.write({'state': 'staging'})

    def action_rollback2approved(self):
        for record in self:
            record.state = 'approved'
            record.task_ids.write({'is_update': False})
            record.pr_ids.write({'state': 'uat'})


    def action_rollback2pending(self):
        for record in self:
            record.state = 'pending'

    def action_rollback2draft(self):
        for record in self:
            record.state = 'draft'

    def action_view_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('id', 'in', self.task_ids.ids)],
            'context': {'default_project_id': self.project_id.id},
        }

    def action_view_pull_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pull Requests',
            'view_mode': 'tree,form',
            'res_model': 'prj.pull.request',
            'domain': [('id', 'in', self.pr_ids.ids)],
        }
