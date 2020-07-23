# -*- coding: utf-8 -*-

{
    'name': 'Student Registration',
    'category': 'Website',
    'version': '1.0',
    'summary': 'Manage your college student registrations',
    'description': "This module allows prospective students register on your website and lets you keep track of the submissions easily.",
    'depends': ['base', 'contacts', 'website'],
    'data': [
        'data/config_data.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
    ],
}
