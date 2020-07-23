# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Student(models.Model):
    _name = 'sure_success.student'
    _description = 'Student'

    name = fields.Char()
    email = fields.Char()
    mobile = fields.Char()
    age = fields.Integer()
    intro = fields.Text("Short Introduction")