# -*- coding: utf-8 -*-
# from odoo import http


# class ECommerceSale(http.Controller):
#     @http.route('/e_commerce_sale/e_commerce_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/e_commerce_sale/e_commerce_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('e_commerce_sale.listing', {
#             'root': '/e_commerce_sale/e_commerce_sale',
#             'objects': http.request.env['e_commerce_sale.e_commerce_sale'].search([]),
#         })

#     @http.route('/e_commerce_sale/e_commerce_sale/objects/<model("e_commerce_sale.e_commerce_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('e_commerce_sale.object', {
#             'object': obj
#         })
