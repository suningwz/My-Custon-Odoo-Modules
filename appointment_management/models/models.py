# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta
import logging
import uuid

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


############# Modification of the Stop field in the calendar.event model ########################################
class Meeting(models.Model):
    _inherit = 'calendar.event'

    stop = fields.Datetime(
        'Stop', required=False, help="Stop date of an event, without time for full days events")
    appointment_id = fields.Char(default=lambda x: uuid.uuid4(), editable=False)
    displayed_appointment_id = fields.Char(compute="_compute_appointment_id")

    @api.depends('name')
    def _compute_appointment_id(self):
        for event in self:
            event.displayed_appointment_id = event.appointment_id[:6]


class Schedule(models.Model):
    _name = 'calendar.schedule'
    _description = "Calendar Schedule"
    _order = "id desc"

    def _get_duration(self, start, stop):
        """ Get the duration value between the 2 given dates. """
        if start and stop:
            diff = fields.Datetime.from_string(
                stop) - fields.Datetime.from_string(start)
            if diff:
                duration = float(diff.days) * 24 + (float(diff.seconds) / 3600)
                return round(duration, 2)
            return 0.0

    name = fields.Char(string="Oggetto", default="Disponibile", editable=False)
    start = fields.Datetime(
        'Start', required=True, help="Start date of an event, without time for full days events")
    stop = fields.Datetime(
        'Stop', required=True, help="Stop date of an event, without time for full days events")

    start_datetime = fields.Datetime('Start DateTime', compute='_compute_dates', inverse='_inverse_dates', store=True,
                                     tracking=True)
    stop_datetime = fields.Datetime('End Datetime', compute='_compute_dates', inverse='_inverse_dates', store=True,
                                    tracking=True)  # old date_deadline
    start_date = fields.Date()
    stop_date = fields.Date()
    duration = fields.Float('Duration')
    available = fields.Boolean(string='Disponibile', default=True)

    @api.depends('start', 'stop')
    def _compute_dates(self):
        for schedule in self:
            schedule.start_datetime = schedule.start
            schedule.start_date = schedule.start.date()
            schedule.stop_datetime = schedule.stop
            schedule.stop_date = schedule.stop.date()
            schedule.duration = self._get_duration(schedule.start, schedule.stop)

    def _inverse_dates(self):
        for schedule in self:
            schedule.write({'start': schedule.start_datetime,
                               'stop': schedule.stop_datetime})

    @api.onchange('start_datetime', 'duration')
    def _onchange_duration(self):
        if self.start_datetime:
            start = self.start_datetime
            self.start = self.start_datetime
            # Round the duration (in hours) to the minute to avoid weird situations where the event
            # stops at 4:19:59, later displayed as 4:19.
            self.stop = start + timedelta(minutes=round(self.duration * 60))
            
    @api.model
    def create(self, values):
        # compute duration, if not given
        if not 'duration' in values:
            values['duration'] = self._get_duration(
                values['start'], values['stop'])
        
        values['name'] = "Disponibile"

        return super(Schedule, self).create(values)
