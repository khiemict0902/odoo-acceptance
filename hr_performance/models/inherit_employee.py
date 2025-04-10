from odoo import fields, models, api


class InheritedEmployee(models.Model):
    _inherit = 'hr.employee'

    review_ids = fields.One2many('hr.performance.review', 'employee_id', string='Người đánh giá')
    average_score = fields.Char('Điểm đánh giá trung bình', compute='_compute_score')

    @api.depends('review_ids')
    def _compute_score(self):
        for record in self:
            list_state = record.review_ids.mapped('state')
            list_score = record.review_ids.mapped('performance_score')
            list_score = [int(i) for i in list_score]
            check = [(x,y) for x,y in zip(list_state, list_score)]
            score = 0
            count = 0
            for i in check:
                if i[0] == 'approved':
                    score += i[1]
                    count += 1
            score =round(score/count) if count else 0
            # print(round(score/count))

            score_value = dict(record.review_ids[-1]._fields['performance_score'].selection).get(str(score)) if score else 0
            record.average_score = score_value