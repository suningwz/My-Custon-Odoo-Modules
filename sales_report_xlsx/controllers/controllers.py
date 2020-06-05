# -*- coding: utf-8 -*-
# from odoo import http


# class SalesReportXlsx(http.Controller):
#     @http.route('/sales_report_xlsx/sales_report_xlsx/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_report_xlsx/sales_report_xlsx/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_report_xlsx.listing', {
#             'root': '/sales_report_xlsx/sales_report_xlsx',
#             'objects': http.request.env['sales_report_xlsx.sales_report_xlsx'].search([]),
#         })

#     @http.route('/sales_report_xlsx/sales_report_xlsx/objects/<model("sales_report_xlsx.sales_report_xlsx"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_report_xlsx.object', {
#             'object': obj
#         })
