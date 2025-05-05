from odoo import api, fields, models
from odoo.exceptions import UserError


class PullRequest(models.Model):
    _name = 'prj.pull.request'
    _description = 'Pull Request của dự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _sql_constraints = [('pr_unique_name','UNIQUE(name)','Tên bản ghi đã tồn tại'),
                        ('pr_unique_linkpr','UNIQUE(link_pr)','Link Pull request đã tồn tại')]


    name = fields.Char('Tên', tracking=True)
    description = fields.Text('Mô tả', tracking=True)
    tags_ids = fields.Many2many('project.tags', string='Thẻ tags', tracking=True)
    link_pr = fields.Char('Link pull request', help="Link phải có dạng 'https://_/pull/_id'", tracking=True)
    id_pr = fields.Char('ID Pull Request', compute='_compute_id_pr', store=True)
    state = fields.Selection([('samdev', 'Samdev'),
                              ('uat', 'UAT'),
                              ('staging', 'Staging'),
                              ('product', 'Production')
                              ], 'Trạng thái', default='samdev', tracking=True)

    prev_state = fields.Selection([
        ('samdev', 'Samdev'),
        ('uat', 'UAT'),
        ('staging', 'Staging'),
        ('product', 'Production'),
    ], string='Trạng thái trước đó')

    person_create_id = fields.Many2one('res.users', string='Người tạo', default=lambda self: self.env.user, tracking=True)
    task_id = fields.Many2one('project.task', 'Nhiệm vụ', required=True, tracking=True)

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

    def open_pull_request_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pull Request',
            'view_mode': 'form',
            'res_model': 'prj.pull.request',
            'res_id': self.id,
            'target': 'current',
        }

    def action_open_task(self):
        self.ensure_one()
        if not self.task_id:
            raise UserError("Không có nhiệm vụ nào được liên kết với pull request này.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Nhiệm vụ',
            'res_model': 'project.task',
            'res_id': self.task_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        if not vals.get('name') and vals.get('task_id'):
            task = self.env['project.task'].browse(vals['task_id'])

            record = super().create(vals)
            record.name = f"PR #{record.id} - {task.name}"
            return record
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if not record.name and record.task_id:
                record.name = f"PR #{record.id} - {record.task_id.name}"
        return res

