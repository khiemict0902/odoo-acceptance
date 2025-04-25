from odoo import api, fields, models
from odoo.exceptions import UserError

class InheritTask(models.Model):
    _inherit = 'project.task'

    pr_ids = fields.One2many('prj.pull.request','task_id','Pull Requests')
    is_update = fields.Boolean(default=False)
    is_close = fields.Boolean(default=False)

    def action_rollback_code(self):
        for task in self:
            if task.is_update:
                for pr in task.pr_ids:
                    if pr.prev_state:
                        pr.state = pr.prev_state
                task.is_update = False

                plans = self.env['prj.update.plan'].search([
                    ('task_ids', 'in', task.id),
                    ('state', 'in', ['done'])
                ])
                for plan in plans:
                    plan.state = 'approved'


            else:
                raise UserError("Nhiệm vụ này chưa được cập nhật, không cần rollback.")
