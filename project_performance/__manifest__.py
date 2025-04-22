{
    'name': 'Quy trình update hệ thống',
    'description': 'Module theo dõi quy trình update hệ thống',
    'category': 'Category',
    'depends': ['base','project','mail'],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/prj_pull_request_view.xml',
            'views/prj_update_plan_view.xml',
            'views/inherit_task_view.xml',
             'views/menu.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': True
}
