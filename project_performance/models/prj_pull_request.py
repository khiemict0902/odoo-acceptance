from odoo import api, fields, models 

class PullRequest(models.Model):
    _name = 'prj.pull.request'
    _description = 'Pull Request của dự án'
    _sql_constraints = [('pr_unique_name','UNIQUE(name)','Tên bản ghi đã tồn tại'),
                        ('pr_unique_linkpr','UNIQUE(link_pr)','Link Pull request đã tồn tại')]


    name = fields.Char('Tên', required=True)
    description = fields.Text('Mô tả')
    tags_ids = fields.Many2many('project.tags', string='Thẻ tags')
    link_pr = fields.Char('Link pull request', help="Link phải có dạng 'https://_/pull/_id'")
    id_pr = fields.Char('ID Pull Request', compute='_compute_id_pr', store=True)
    state = fields.Selection([('samdev', 'Samdev'),
                              ('uat', 'UAT'),
                              ('staging', 'Staging'),
                              ('product', 'Production')
                              ], 'Trạng thái', default='samdev')
    person_create_id = fields.Many2one('res.users', string='Người tạo', default=lambda self: self.env.user)
    date_create = fields.Date(string='Ngày tạo', default=fields.Date.today)

    @api.depends('link_pr')
    def _compute_id_pr(self):
        for pull in self:
            if "pull/" in pull.link_pr:
                pull.id_pr = pull.link_pr.split('/')[-1]
            else:
                pull.id_pr = False
