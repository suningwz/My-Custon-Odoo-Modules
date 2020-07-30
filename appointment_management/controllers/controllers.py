# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from datetime import datetime


class AppointmentManagement(http.Controller):
    @http.route('/appointment-management', type='http', auth="public", website=True, csrf=False)
    def appointment(self, **kw):
        return request.render('appointment_management.appointment_form')

    @http.route('/schedule', type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def schedule(self, **kw):
        date = request.params['date']
        # search for all the records with out filtering
        schedules = http.request.env['calendar.schedule'].sudo().search([])

        for schedule in schedules:
            if str(schedule.start_date) == str(date):
                obj = {
                    'start_date': str(schedule.start_date),
                    'stop_date': str(schedule.stop_date),
                    'start_datetime': str(schedule.start_datetime),
                    'stop_datetime': str(schedule.stop_datetime),
                    'duration': str(schedule.duration),
                    'info': 'Available'
                }
                return json.dumps(obj)
            elif str(schedule.start_datetime).split(sep=' ')[0] == str(date):
                obj = {
                    'start_date': str(schedule.start_date),
                    'stop_date': str(schedule.stop_date),
                    'start_datetime': str(schedule.start_datetime),
                    'stop_datetime': str(schedule.stop_datetime),
                    'duration': str(schedule.duration),
                    'info': 'Available'
                }
                return json.dumps(obj)
            else:
                obj = {
                    'start_date': 'False',
                    'stop_date': 'False',
                    'start_datetime': 'False',
                    'stop_datetime': 'False',
                    'duration': 'False',
                    'info': 'Not Available'
                }
                return json.dumps(obj)

    @http.route('/appointment-management/new', type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def new_appointment(self, **kw):
        date = request.params['date']
        time = request.params['time']
        converted_date = datetime.strptime(f'{date} {time}:00', '%Y-%m-%d %H:%M:%S')

        record = http.request.env['calendar.event']
        record.sudo().create({
            'name': 'Appointment',
            'start': converted_date,
            'stop': converted_date,
            'start_datetime': converted_date,
            'duration': '00.30'
        })
        return request.redirect('/appointment-booked')

    @http.route('/appointment-booked', type='http', auth="public", website=True, csrf=False)
    def appointment_booked(self, **kw):
        return request.render('appointment_management.appointment_confirmation')

