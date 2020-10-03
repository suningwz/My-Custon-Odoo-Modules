# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits='Product Price', groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
        In FIFO: value of the last unit that left the stock (automatically computed).
        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
        Used to compute margins on sale orders.""")

    sale_ok = fields.Boolean('Can be Sold', default=False)
    purchase_ok = fields.Boolean('Can be Purchased', default=False)

    @api.depends_context('force_company')
    @api.depends('product_variant_ids', 'product_variant_ids.standard_price', 'sale_ok')
    def _compute_standard_price(self):
        # Depends on force_company context because standard_price is company_dependent
        # on the product_product
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.standard_price = template.product_variant_ids.standard_price
        for template in (self - unique_variants):
            template.standard_price = 0.0

        price = 0.0
        for product in self:
            if product.sale_ok:
                for recipe in product.recipes:
                    if recipe.final_product == product:
                        for reciprods in recipe.ingredient:
                            price += reciprods.standard_price
                product.standard_price = price

    def _set_standard_price(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.standard_price = template.standard_price

    def _search_standard_price(self, operator, value):
        products = self.env['product.product'].search([('standard_price', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]

