# -*- coding: utf-8 -*-
# from odoo import http


# class Person(http.Controller):
#     @http.route('/person/person/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/person/person/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('person.listing', {
#             'root': '/person/person',
#             'objects': http.request.env['person.person'].search([]),
#         })

#     @http.route('/person/person/objects/<model("person.person"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('person.object', {
#             'object': obj
#         })
