from odoo import models

class HrLeaveManager(models.Model):
    _inherit = 'hr.leave'

    def action_approve_batch(self):
        for record in self:
            record.state = 'validate'
