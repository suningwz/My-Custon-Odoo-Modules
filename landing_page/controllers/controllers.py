# -*- coding: utf-8 -*-

import base64 as b, smtplib
from email.message import EmailMessage
from odoo import http, fields, _
from odoo.exceptions import UserError
from odoo.http import request, werkzeug


class Website(http.Controller):
    @http.route(['/page/landing-page/backyard'], auth="public", website=True)
    def backyard(self):
        return werkzeug.utils.redirect("/landing_page/static/src/backyard.html")

    @http.route(['/page/landing-page/oneschool'], auth="public", website=True)
    def oneschool(self):
        return werkzeug.utils.redirect("/landing_page/static/src/oneschool.html")

    @http.route(['/page/landing-page/unfold'], auth="public", website=True)
    def unfold(self):
        return werkzeug.utils.redirect("/landing_page/static/src/unfold.html")

    @http.route(['/landing_page/static/src/furnish.html'], auth="public", website=True)
    def furnish(self):
        return werkzeug.utils.redirect("/landing_page/static/src/furnish.html")



    @http.route(['/page/landing-page/submit-message'], auth="public", website=True)
    def home(self, **kwargs):
        fromaddr = kwargs["name"] + " <no-reply@foreverehiorobo.com>"
        toaddrs = "ehioroboevans@gmail.com"
        SMTPServer = 'ns55.stableserver.net'
        port = 465
        arg1 = "sender@foreverehiorobo.com"
        arg2 = "zVSzjf26rLain8i"

        msg = EmailMessage()
        msgtxt = (
            kwargs["body"] + "\n\n" +
                kwargs["name"] + "\n" +
                    kwargs["phone"] + "\n" +
                        kwargs["email"]
        )
        msg.set_content(msgtxt)
        msg['Subject'] = "New Message from " + kwargs["name"]
        msg['From'] = fromaddr
        msg['To'] = toaddrs

        server = smtplib.SMTP_SSL(SMTPServer, port)
        server.login(arg1, arg2)
        server.send_message(msg)
        server.quit()

        return werkzeug.utils.redirect(kwargs["from"])