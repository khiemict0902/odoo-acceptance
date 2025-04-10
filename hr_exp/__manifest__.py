{
    'name': 'HR Experiment',
    # 'version': 'Version',
    # 'summary': 'Summery',
    'description': 'Description',
    'category': 'Category',
    # 'author': 'Author',
    # 'website': 'Website',
    # 'license': 'License',
    'depends': ['base','hr','mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/exp_wizard_view.xml',
        'views/inherit_employee_view.xml',
             ],
    # 'demo': ['demo/hr_performance_review.xml'],
    'installable': True,
    'application': True,
    'auto_install': True
}
