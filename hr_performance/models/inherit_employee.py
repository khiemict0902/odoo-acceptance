from odoo import fields, models, api


class InheritedEmployee(models.Model):
    _inherit = 'hr.employee'

    review_ids = fields.One2many('hr.performance.review', 'employee_id', string='Người đánh giá')
    average_score = fields.Char('Điểm đánh giá trung bình', compute='_compute_score')

    @api.depends('review_ids')
    def _compute_score(self):
        for record in self:
            list_review = record.review_ids.filtered(lambda r: r.state == 'approved')
            scores = [int(r.performance_score) for r in list_review if r.performance_score]

            if scores:
                average = round(sum(scores) / len(scores))
                score_value = dict(record.review_ids[0]._fields['performance_score'].selection).get(str(average))
            else:
                score_value = 0

            record.average_score = score_value
