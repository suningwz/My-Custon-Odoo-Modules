# -*- coding: utf-8 -*-
# from odoo import http


# class RecipeMgt(http.Controller):
#     @http.route('/recipe_mgt/recipe_mgt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/recipe_mgt/recipe_mgt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('recipe_mgt.listing', {
#             'root': '/recipe_mgt/recipe_mgt',
#             'objects': http.request.env['recipe_mgt.recipe_mgt'].search([]),
#         })

#     @http.route('/recipe_mgt/recipe_mgt/objects/<model("recipe_mgt.recipe_mgt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('recipe_mgt.object', {
#             'object': obj
#         })
