# -*- coding: utf-8 -*-
# from odoo import http


# class Mailer(http.Controller):
#     @http.route('/mailer/mailer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mailer/mailer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mailer.listing', {
#             'root': '/mailer/mailer',
#             'objects': http.request.env['mailer.mailer'].search([]),
#         })

#     @http.route('/mailer/mailer/objects/<model("mailer.mailer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mailer.object', {
#             'object': obj
#         })
