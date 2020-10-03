# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PullOrders(models.Model):
    _name = 'pull.orders'
    _description = 'This pulls orders from specified APIs and create new sales order quotation'
