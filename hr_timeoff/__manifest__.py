{
    'name': 'HR Time off Manager',
    # 'version': 'Version',
    # 'summary': 'Summery',
    'description': 'Description',
    'category': 'Category',
    # 'author': 'Author',
    # 'website': 'Website',
    # 'license': 'License',
    'depends': ['base','hr','mail','hr_holidays'],
    'data': [
            'security/ir.model.access.csv',
            'views/hr_leave_manager.xml',
             'wizard/leave_batchupdate_wizard_view.xml',
             # 'views/menu.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': True
}
