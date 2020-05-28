# -*- coding: utf-8 -*-

from odoo import models, fields, api


class person(models.Model):
    _name = 'person.person'
    _description = 'Personal Details'

    name = fields.Char(string='Full Name')
    image = fields.Binary(string='Profile Photo')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    company = fields.Char(string='Work Company Name')

    def send_mail(self):
        template_id = self.env.ref('person.person_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
