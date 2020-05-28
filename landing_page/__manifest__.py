# -*- coding: utf-8 -*-
{
    'name': "Landing Pages",

    'summary': """
        Simple and beautifully designed landing pages""",

    'description': """
    """,

    'author': "Evans Ehiorobo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}