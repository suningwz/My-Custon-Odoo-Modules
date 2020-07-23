# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hospital_consent_forms(models.Model):
    _name = 'hospital.consent.form'
    _description = 'hospital consent forms'

    consent_form = fields.Html(string='Consent Form')


class hospital_visit_inherit(models.Model):
    _inherit = 'hospital.visit'

    consent_form_signature = fields.Binary(string='Signature')
