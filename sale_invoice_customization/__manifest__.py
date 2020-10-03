# -*- coding: utf-8 -*-
{
    'name': "Sale, Invoice and Delivery Customization",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'product', 'account', 'stock', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/report_views.xml',
        'views/report_package_barcode.xml',
        'views/report_invoice.xml',
        'views/report_sale_order.xml',
        'views/report_purchase_order.xml',
    ],
}
