{
    'name': 'HR Performance',
    # 'version': 'Version',
    # 'summary': 'Summery',
    'description': 'Description',
    'category': 'Category',
    # 'author': 'Author',
    # 'website': 'Website',
    # 'license': 'License',
    'depends': ['base','hr','mail'],
    'data': ['security/hr_performance_security.xml',
             'security/hr_p_rules.xml',
             'security/ir.model.access.csv',
             'demo/hr_performance_review.xml',
             'views/hr_performance_review_view.xml',
             'views/inherit_employee_view.xml',
             'views/menu.xml',
             ],
    'demo': ['demo/hr_performance_review.xml'],
    'installable': True,
    'application': True,
    'auto_install': True
}
