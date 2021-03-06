# -*- coding: utf-8 -*-
{
    'name': "Appointment Management",

    'summary': """
        This module helps to schedule and manage appointments for professionals.""",

    'description': """
        This module helps to schedule and manage appointments for professionals.
    """,

    'author': "Evans Ehiorobo",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Calendar',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar', 'mail', 'website'],

    # always loaded
    'data': [
        'data/config_data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
