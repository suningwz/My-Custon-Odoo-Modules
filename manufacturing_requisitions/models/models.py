# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class manufacturing_requisitions(models.Model):
    _name = 'manufacturing.requisitions'
    _description = 'manufacturing requisitions'

    name = fields.Char(string='Requisition #', readonly=True,)
    vendor = fields.Many2one(comodel_name='res.partner', string='Vendor')
    show_only_this_vendors_material = fields.Boolean()
    associate_with_project = fields.Many2one(comodel_name='manufacturing.project')
    po_num = fields.Integer(string='PO #')
    order_by = fields.Date()
    needed_by = fields.Date()
    comment = fields.Text()
    material_requisition = fields.One2many(comodel_name='manufacturing.material.requisition', inverse_name='manufacturing_requisitions')
    requested_by = fields.Many2one(comodel_name='res.users')
    state = fields.Char()

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('manufacturing.requisitions')
        return super(manufacturing_requisitions, self).create(vals)


class manufacturing_project(models.Model):
    _name = 'manufacturing.project'
    _description = 'manufacturing projects'

    name = fields.Char()


class manufacturing_material_requisition(models.Model):
    _name = 'manufacturing.material.requisition'
    _description = 'manufacturing material requisition'

    part_no = fields.Integer(string='Part #')
    material_name = fields.Char()
    material_id = fields.Char()
    version = fields.Integer()
    material_unit = fields.Many2one(comodel_name='uom.uom')
    vendor_part_no = fields.Integer(string='Vendor Part #')
    vendor_catalog_no = fields.Integer(string='Vendor Catalog #')
    cost_per_unit = fields.Float()
    quantity = fields.Float()
    unit = fields.Many2one(comodel_name='uom.uom')
    msds = fields.Boolean(string='MSDS')
    c_of_a = fields.Boolean(string='C of A')
    manufacturing_requisitions = fields.Many2one(comodel_name='manufacturing.requisitions')
