# -*- coding: utf-8 -*-

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi

from odoo import http
from odoo.http import request
import json
from datetime import datetime, timedelta
from dateutil import relativedelta

def abort_and_redirect(url):
    r = request.httprequest
    response = werkzeug.utils.redirect(url, 302)
    response = r.app.get_response(r, response, explicit_session=False)
    werkzeug.exceptions.abort(response)

def ensure_db(redirect='/web/database/selector'):
    # This helper should be used in web client auth="none" routes
    # if those routes needs a db to work with.
    # If the heuristics does not find any database, then the users will be
    # redirected to db selector or any url specified by `redirect` argument.
    # If the db is taken out of a query parameter, it will be checked against
    # `http.db_filter()` in order to ensure it's legit and thus avoid db
    # forgering that could lead to xss attacks.
    db = request.params.get('db') and request.params.get('db').strip()
    
    # Ensure db is legit
    if db and db not in http.db_filter([db]):
        db = None

    if db and not request.session.db:
        # User asked a specific database on a new session.
        # That mean the nodb router has been used to find the route
        # Depending on installed module in the database, the rendering of the page
        # may depend on data injected by the database route dispatcher.
        # Thus, we redirect the user to the same page but with the session cookie set.
        # This will force using the database route dispatcher...
        r = request.httprequest
        url_redirect = werkzeug.urls.url_parse(r.base_url)
        if r.query_string:
            # in P3, request.query_string is bytes, the rest is text, can't mix them
            query_string = iri_to_uri(r.query_string)
            url_redirect = url_redirect.replace(query=query_string)
        request.session.db = db
        abort_and_redirect(url_redirect)

    # if db not provided, use the session one
    if not db and request.session.db and http.db_filter([request.session.db]):
        db = request.session.db

    # if no database provided and no database in session, use monodb
    if not db:
        db = db_monodb(request.httprequest)

    # if no db can be found til here, send to the database selector
    # the database selector will redirect to database manager if needed
    if not db:
        # werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))
        pass

    # always switch the session to the computed db
    if db != request.session.db:
        request.session.logout()
        abort_and_redirect(request.httprequest.url)

    request.session.db = db

class Schedule():
    '''
    Schedule class to be used when sorting the already scheduled times from older to newer.
    '''
    def __init__(self, obj):
        self.obj = obj

    def _get_hour(self):
        return int(self.obj["start_datetime"].split(" ")[1].split(":")[0])

    def __lt__(self, other):
        return self._get_hour() < other._get_hour()

    def __gt__(self, other):
        return self._get_hour() > other._get_hour()

    def __eq__(self, other):
        return self._get_hour() == other._get_hour()


class AppointmentManagement(http.Controller):
    @http.route('/appointment-management', type='http', auth="public", website=True, csrf=False)
    def appointment(self, **kw):
        ensure_db()
        return request.render('appointment_management.appointment_form', {
            'error': ''
        })

    @http.route('/schedule', type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def schedule(self, **kw):
        date = request.params['date']
        # search for all the records with out filtering
        schedules = http.request.env['calendar.schedule'].sudo().search([('start_date', '=', date)])
        objs = []

        for schedule in schedules:
            objs.append(Schedule({
                'start_datetime': str(schedule.start_datetime),
                'stop_datetime': str(schedule.stop_datetime),
                'picked_times': [str(event.start) for event in
                    http.request.env['calendar.event'].sudo().search([])
                    if str(event.start_datetime).split(" ")[0] == str(schedule.start_datetime).split(" ")[0]
                ]
            }))
        
        objs.sort()
        objs = [item.obj for item in objs]
        
        return json.dumps(objs)

    @http.route('/appointment-management/new', type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def new_appointment(self, **kw):
        date = request.params['date']
        time = request.params['time']
        converted_date = datetime.strptime(f'{date} {time}:00', '%Y-%m-%d %H:%M:%S')
        stop_datetime = datetime.strptime(f'{date} {time}:00', '%Y-%m-%d %H:%M:%S') + timedelta(minutes=30)        
        
        record = http.request.env['calendar.event']
        try:
            rec_id = record.sudo().create({
                'name': 'Appuntamenti',
                'start': converted_date,
                'stop': stop_datetime
            })
            time = str(int(time.split(":")[0]) + 1) + ":" + time.split(":")[1]
            return request.render('appointment_management.appointment_confirmation', {
                'id': rec_id.displayed_appointment_id,
                'date': date,
                'time': time
            })
        except:
            return request.render('appointment_management.appointment_form', {
                'error': 'An error occurred while booking your appointment. Please try again.'
            })