# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json


class Product_Product(models.Model):
    _inherit = 'product.product'

    sku = fields.Char(string="SKU")

    @api.model
    def create(self, vals):

        res = super(Product_Product, self).create(vals)
        print(vals)
        j_data = json.dumps({
            'list_price': str(vals['lst_price']),
            'sku': str(vals['sku']),
            'product_id': '',
            'stock_qty': '',

        })
        requests.post('http://localhost:8069/shopify/order/post', data=j_data)
        return res

    def write(self, vals):
        res = super(Product_Product, self).write(vals)
        print(vals)
        j_data = json.dumps({
            'sku': str(vals['sku']),
            'product_id': '',
            'stock_qty': '',
            'list_price': str(vals['lst_price'])
        })
        requests.post('http://localhost:8069/shopify/order/post', data=j_data)
        return res




# class Product_Template(models.Model):
#     _inherit = 'product.template'
#
#     sku = fields.Char(string="SKU")
