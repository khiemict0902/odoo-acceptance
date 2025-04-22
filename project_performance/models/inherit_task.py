from odoo import api, fields, models

class InheritTask(models.Model):
    _inherit = 'project.task'

    pr_ids = fields.One2many('prj.pull.request','task_id','Pull Requests')
    is_update = fields.Boolean(default=False)