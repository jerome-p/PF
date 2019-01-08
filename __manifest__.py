# -*- coding: utf-8 -*-
{
    'name': "PureFitness Client Information",

    'summary': """
        Adds client information to contacts page""",

    'description': """
        Adds client information to contacts page
        """,

    'author': "Jerome",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts',],
    # always loaded
    'data': [
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
}
