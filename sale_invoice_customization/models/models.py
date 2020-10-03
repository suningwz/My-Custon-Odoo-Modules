# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


# extending the purchase
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_po = fields.Many2one(
        string="Client's PO#", comodel_name='purchase.order')


class Invoice(models.Model):
    _inherit = 'account.move'

    client_po = fields.Many2one(
        'purchase.order', string="Client's PO#", compute="_compute_client_po")

    @api.depends('invoice_origin')
    def _compute_client_po(self):
        for move in self:
            order = None

            if move.type == "out_invoice":
                order = move.env['sale.order'].search(
                    [('name', '=', move.invoice_origin)], limit=1)
            elif move.type == "in_invoice":
                order = move.env['purchase.order'].search(
                    [('name', '=', move.invoice_origin)], limit=1)
            
            if order:
                move.client_po = order.client_po
            else:
                move.client_po = False


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    client_po = fields.Many2one(
        'purchase.order', string="Client's PO#", compute="_compute_client_po")

    @api.depends('origin')
    def _compute_client_po(self):
        for picking in self:
            order = picking.env['sale.order'].search(
                [('name', '=', picking.origin)], limit=1)
            if order:
                picking.client_po = order.client_po
            else:
                picking.client_po = False


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    case_qty = fields.Float(string="Case Qty", compute='_compute_case_qty')
    package = fields.Float(string="Package Qty",
                           related='product_id.packaging_ids.qty')

    @api.depends('product_uom_qty', 'package')
    def _compute_case_qty(self):
        for line in self:
            if line.package != 0:
                line.case_qty = line.product_uom_qty / line.package
            else:
                line.case_qty = line.product_uom_qty


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    case_qty = fields.Float(string="Case Qty", compute='_compute_case_qty')
    package = fields.Float(string="Package Qty",
                           related='product_id.packaging_ids.qty')

    @api.depends('product_qty', 'package')
    def _compute_case_qty(self):
        for line in self:
            if line.package != 0:
                line.case_qty = line.product_qty / line.package
            else:
                line.case_qty = line.product_qty


class StockMove(models.Model):
    _inherit = 'stock.move'

    case_qty_demand = fields.Float(compute='_compute_case_qty_demand')
    case_qty_reserved = fields.Float(compute='_compute_case_qty_reserved')
    case_qty_done = fields.Float(compute='_compute_case_qty_done')

    @api.depends('product_uom_qty', 'product_id.packaging_ids.qty')
    def _compute_case_qty_demand(self):
        for move in self:
            if move.product_id.packaging_ids.qty:
                move.case_qty_demand = move.product_uom_qty / move.product_id.packaging_ids.qty
            else:
                move.case_qty_demand = move.product_uom_qty

    @api.depends('reserved_availability', 'product_id.packaging_ids.qty')
    def _compute_case_qty_reserved(self):
        for move in self:
            if move.product_id.packaging_ids.qty:
                move.case_qty_reserved = move.reserved_availability / \
                    move.product_id.packaging_ids.qty
            else:
                move.case_qty_reserved = move.reserved_availability

    @api.depends('quantity_done', 'product_id.packaging_ids.qty')
    def _compute_case_qty_done(self):
        for move in self:
            if move.product_id.packaging_ids.qty:
                move.case_qty_done = move.quantity_done / move.product_id.packaging_ids.qty
            else:
                move.case_qty_done = move.quantity_done


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    # ordered_qty = fields.Float()
    # case_qty = fields.Float(compute='_compute_case_qty')
    invoiced_case_qty = fields.Float(compute='_compute_invoiced_case_qty')
    package = fields.Float(string="Package", related='product_id.packaging_ids.qty')

    # @api.depends('purchase_line_id.product_uom_qty', 'package')
    # def _compute_case_qty(self):
    #     for line in self:
    #         move = line.move_id
    #         order = None

    #         if move.type == "out_invoice":
    #             order = move.env['sale.order'].search(
    #                 [('name', '=', move.invoice_origin)], limit=1)
    #         elif move.type == "in_invoice":
    #             order = move.env['purchase.order'].search(
    #                 [('name', '=', move.invoice_origin)], limit=1)
            
    #         if line.package:
    #             line.case_qty = line.ordered_qty / line.package
    #         else:
    #             line.case_qty = line.ordered_qty

    @api.depends('quantity', 'package')
    def _compute_invoiced_case_qty(self):
        for line in self:
            if line.package:
                line.invoiced_case_qty = line.quantity / line.package
            else:
                line.invoiced_case_qty = line.quantity


# model for package slip
class StockPackage(models.Model):
    _inherit = 'stock.quant.package'

    client_po = fields.Many2one('purchase.order', string="Client's PO#")
    print_date = fields.Date(string='Printing Date',
                             compute='_compute_print_date')
    ship_to = fields.Char()
    ship_from = fields.Char()

    @api.depends('name')
    def _compute_print_date(self):
        for package in self:
            package.print_date = datetime.today().strftime('%Y-%m-%d')
