# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import request


class HospitalConsentForms(http.Controller):

    @http.route('/hospital/consent-form', type='http', auth="public", website=True, csrf=False)
    def consent_form(self, **kw):
        consent = http.request.env['hospital.consent.form'].sudo().search([])
        return http.request.render('hospital_consent_forms.consent_form', {
            'consent': consent[0]
        })

    @http.route('/hospital/submit-consent', type='http', auth="public", methods=["POST"], website=True, csrf=False)
    def submit_consent(self, **kw):
        signature = request.httprequest.files['signature']
        obj = request.env['hospital.visit'].sudo().search([])
        img = signature.read()
        if obj:
            obj[0].sudo().write({
                'consent_form_signature': base64.b64encode(img)
            })
            return http.request.render('hospital_consent_forms.consent_form_response', {
                'response': 'Success',
            })
        else:
            print('No object')
