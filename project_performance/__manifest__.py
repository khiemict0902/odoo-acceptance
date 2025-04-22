{
    'name': 'Dự án hieu suat',
    'description': 'Description',
    'category': 'Category',
    'depends': ['base','project'],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/prj_pull_request_view.xml',
            'views/prj_update_plan_view.xml',
            'views/inherit_task_view.xml',
             # 'wizard/leave_batchupdate_wizard_view.xml',
             'views/menu.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': True
}
