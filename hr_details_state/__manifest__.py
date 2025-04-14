{
    'name': 'HR Appicant Detail State',
    'description': 'Description',
    'category': 'Category',
    'depends': ['base','hr','mail','hr_recruitment'],
    'data': [
             'security/ir.model.access.csv',
             'views/inherit_applicant.xml',
             'views/details_state.xml',
             'views/menu.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': True
}
