# -*- coding: utf-8 -*-

from odoo import models, fields, api, osv


class AutoBuy(models.Model):
    _name = "autobuy.autobuy"
    #  _rec_name = 'service'
    _description = "AutoBuy Customers"

    name = fields.Char(string='Year', required=True),
    make = fields.Char(string='Make', required=True),
    car_model = fields.Char(string='Model', required=True),
    service = fields.Char(string='Service ID'),

    def onchange_service(self, cr, uid, ids, serviceid=False, context=None):
        res = {}
        if serviceid:
            service_obj = self.pool.get('auto.buy')
            rec = service_obj.browse(cr, uid, serviceid)
            res = {'value': {'name': rec.name, 'model': rec.model, 'make': rec.make}}
        else:
            res = {'value': {'name': False, 'model': False, 'make': False}}
        return res


#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class servicesales(models.Model):
    _name = "service.sale"
    _description = "service"

    name = fields.Char('Year', required=True),
    make = fields.Char('Make', required=True),
    car_model = fields.Char('Model', required=True),
    serviceid = fields.Many2one('autobuy.autobuy', 'Service ID', select=True),

