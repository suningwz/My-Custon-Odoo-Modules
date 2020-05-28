# -*- coding: utf-8 -*-
# from odoo import http


# class ManufacturingRequisitions(http.Controller):
#     @http.route('/manufacturing_requisitions/manufacturing_requisitions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manufacturing_requisitions/manufacturing_requisitions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('manufacturing_requisitions.listing', {
#             'root': '/manufacturing_requisitions/manufacturing_requisitions',
#             'objects': http.request.env['manufacturing_requisitions.manufacturing_requisitions'].search([]),
#         })

#     @http.route('/manufacturing_requisitions/manufacturing_requisitions/objects/<model("manufacturing_requisitions.manufacturing_requisitions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manufacturing_requisitions.object', {
#             'object': obj
#         })
