# -*- coding: utf-8 -*-
# from odoo import http


# class PendingReceipt(http.Controller):
#     @http.route('/pending_receipt/pending_receipt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pending_receipt/pending_receipt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pending_receipt.listing', {
#             'root': '/pending_receipt/pending_receipt',
#             'objects': http.request.env['pending_receipt.pending_receipt'].search([]),
#         })

#     @http.route('/pending_receipt/pending_receipt/objects/<model("pending_receipt.pending_receipt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pending_receipt.object', {
#             'object': obj
#         })
