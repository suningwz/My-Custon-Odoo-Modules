# -*- coding: utf-8 -*-
# from odoo import http


# class Autobuy(http.Controller):
#     @http.route('/autobuy/autobuy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/autobuy/autobuy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('autobuy.listing', {
#             'root': '/autobuy/autobuy',
#             'objects': http.request.env['autobuy.autobuy'].search([]),
#         })

#     @http.route('/autobuy/autobuy/objects/<model("autobuy.autobuy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('autobuy.object', {
#             'object': obj
#         })
