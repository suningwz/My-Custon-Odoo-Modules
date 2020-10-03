# -*- coding: utf-8 -*-
# from odoo import http


# class OdooConsultingMobileApp(http.Controller):
#     @http.route('/odoo_consulting_mobile_app/odoo_consulting_mobile_app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_consulting_mobile_app/odoo_consulting_mobile_app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_consulting_mobile_app.listing', {
#             'root': '/odoo_consulting_mobile_app/odoo_consulting_mobile_app',
#             'objects': http.request.env['odoo_consulting_mobile_app.odoo_consulting_mobile_app'].search([]),
#         })

#     @http.route('/odoo_consulting_mobile_app/odoo_consulting_mobile_app/objects/<model("odoo_consulting_mobile_app.odoo_consulting_mobile_app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_consulting_mobile_app.object', {
#             'object': obj
#         })
