# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Ingredient_Allergens(models.Model):
    _name = 'recipe.ingredient.allergen'
    _description = 'Recipe management model'

    name = fields.Char('Allergens')


class Ingredient_Groups(models.Model):
    _name = 'recipe.ingredient.group'
    _description = 'Recipe management model'

    name = fields.Char('Group')


#########################################################################################################
class Product(models.Model):
    _inherit = 'product.template'

    group = fields.Many2one(comodel_name='recipe.ingredient.group', string='Group')
    allergens = fields.Many2many(comodel_name='recipe.ingredient.allergen')
    nutrient_code = fields.Char(string='Nutrient Code')
    ingredient_product = fields.One2many(comodel_name='product.template', inverse_name='product_id',
                                         string='Ingredient Composition')
    product_id = fields.Many2one(string='Product')
    vendor = fields.Char(string='Vendor')
    item_code = fields.Char(string='Item Code')
    unit_description = fields.Text('Unit Description')
    recipes = fields.One2many("recipe.recipe", inverse_name="final_product")


#########################################################################################################

class Recipe(models.Model):
    _name = 'recipe.recipe'
    _description = 'The model for adding recipes'

    name = fields.Char(string='Recipe Name')
    type = fields.Many2one(comodel_name='recipe.recipe.type')
    description = fields.Text(string='Description')
    final_product = fields.Many2one("product.template")
    primary_categories = fields.Many2one(comodel_name='recipe.recipe.primary_categories')
    secondary_categories = fields.Many2one(comodel_name='recipe.recipe.secondary_categories')
    ingredient = fields.Many2many(comodel_name='product.template', string='Ingredients')
    allergens = fields.Text(string='Allergens', compute='_compute_allergens')

    @api.depends('ingredient.allergens')
    def _compute_allergens(self):
        allergen = ''
        for records in self.ingredient:
            if records:
                for rec in records.allergens:
                    if rec.name not in allergen: allergen += f'{rec.name}, '
        self.allergens = allergen


class Recipe_Type(models.Model):
    _name = 'recipe.recipe.type'
    _description = 'The model for adding recipes types'

    name = fields.Char(string='Recipe Type')


class Recipe_Primary_Categories(models.Model):
    _name = 'recipe.recipe.primary_categories'
    _description = 'The model for adding recipes categories'

    name = fields.Char(string='Primary Categories')


class Recipe_Secondary_Categories(models.Model):
    _name = 'recipe.recipe.secondary_categories'
    _description = 'The model for adding recipes categories'

    name = fields.Char(string='Secondary Categories')
