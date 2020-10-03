# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.move'

    package = fields.Float(string="Package", related='product_id.packaging_ids.qty')


class Invoice(models.Model):
    _inherit = 'account.move'

    vendor_po = fields.Char(string='Vendor PO#')
