{
    'name': 'HR Ext Manager',
    'description': 'Description',
    'category': 'Category',
    'depends': ['base','hr','mail'],
    'data': [
            'security/security.xml',
            'security/rule.xml',
            'security/ir.model.access.csv',
            'wizard/certification_to_skill_wizard_view.xml',
            'wizard/skill_cert_wizard_view.xml',
            'views/inherit_employee_view.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': True
}
