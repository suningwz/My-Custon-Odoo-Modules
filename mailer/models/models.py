# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mailer(models.Model):
    _name = 'mailer.mailer'
    _description = 'mailer.mailer'

    name = fields.Char(string='Full Name')
    image = fields.Binary(string='Profile Photo')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
