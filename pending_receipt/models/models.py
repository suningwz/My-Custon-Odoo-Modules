# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pending_receipt(models.Model):
    _name = 'manufacturing.pending.receipt'
    _description = 'pending_receipt.pending_receipt'

    receipt_no = fields.Integer(string='Receipt')
    part_no = fields.Integer(string='Part')
    version = fields.Integer()
    material_name = fields.Char()
    material_id = fields.Integer(string='Material ID')
    vendor_name = fields.Char()
    vendor_part_no = fields.Integer(string='Vendor Part')
    project = fields.Char()
    requisition_no = fields.Integer(string='Requisition No')
    po_no = fields.Integer(string='PO')
    qty_ord = fields.Float()
    qty_rcv = fields.Float()
    unit = fields.Many2one('uom.uom')
    # The fields below will not be added to tree view
    upload_receipt = fields.Binary()
    upload_receipt_name = fields.Char()
