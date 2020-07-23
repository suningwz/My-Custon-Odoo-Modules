# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class CollegeRegistration(http.Controller):
    @http.route('/college/register', type='http', auth="public", website=True, csrf=False)
    def register_to_college(self, **kwargs):
        if request.httprequest.method == "GET":
            return request.render("sure_success.apply")
        else:
            print(dir(request))
            print(request.params["partner_name"])
            try:
                request.env['sure_success.student'].sudo().create({
                    "name": request.params["partner_name"],
                    "email": request.params["email_from"],
                    "mobile": str(request.params["partner_phone"]),
                    "age": int(request.params["partner_age"]),
                    "intro": request.params["description"]
                })
            except Exception as e:
                print(e.args)
                return "Error with registration. Please go back and try again"
            return "Registration Successful!"
