from odoo import api, fields, models

class InheritTask(models.Model):
    _inherit = 'project.task'

    pr_id = fields.Many2one('prj.pull.request', string='Dự án')
    is_update = fields.Boolean(default=False)