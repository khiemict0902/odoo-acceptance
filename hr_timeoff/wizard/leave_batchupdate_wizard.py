from odoo import fields, models, api


class LeaveBatchWizard(models.TransientModel):
    _name = 'leave.batchupdate.wizard'
    _description = 'Wizard tùy chỉnh cho phép cập nhật trạng thái nghỉ phép của các bản ghi đã chọn trong tree view'

    state = fields.Selection([('draft','To submit'),
                              ('confirm','To approve'),
                              ('refuse', 'Refused'),
                              ('validate','Approved')], string='Status', required=True)

    def apply_leave_update(self):
        ids = self.env.context['active_ids']
        leaves = self.env['hr.leave'].browse(ids)
        new_data={}
        if self.state:
            new_data['state'] = self.state
        leaves.write(new_data)