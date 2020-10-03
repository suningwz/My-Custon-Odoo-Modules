# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import yaml


# Function to search for customer and create a new one if it doesnt exist
def customer_method(customer):
    try:

        customer_name = f"{customer['first_name']} {customer['last_name']}"
        address = customer['default_address']
        partner = http.request.env['res.partner'].sudo().search([('name', 'ilike', customer_name)])
        if partner:
            return partner.id
        else:
            partner = http.request.env['res.partner'].sudo().create({
                'name': customer_name,
                'email': customer['email'],
                'phone': customer['phone'],
                'street': address['address1'],
                'street2': address['address2'],
                'city': address['city'],
                'zip': address['zip']
            })
            return partner.id
    except:
        return {
            'error': 'An Error Occurred with the customer function'}


def order_lines(items, order):
    try:
        for item in items:
            product = http.request.env['product.product'].sudo().search([('sku', '=', item['sku'])])
            if product:
                http.request.env['sale.order.line'].sudo().create({
                    'order_id': order.id,
                    'name': item['name'],
                    'product_id': product.id,
                    'product_uom_qty': item['quantity'],
                    'price_unit': item['price'],
                    'order_partner_id': order.partner_id.id,
                    'discount': item['total_discount']
                })
            else:
                print('NO Product')
        return http.request.env['sale.order.line'].sudo().search([('order_id', '=', order.id)])
    except:
        return {
            'error': 'An Error Occurred with the order line function'}


class SaleOrder(http.Controller):
    @http.route('/shopify/order', type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def sale_order(self, **kw):
        data = yaml.load(request.httprequest.data)
        if data:
            j_data = data['data']
            try:
                order = http.request.env['sale.order'].sudo().create({
                    'name': j_data['name'],
                    'date_order': j_data['created_at'],
                    'amount_total': j_data['total_price'],
                    'partner_id': customer_method(j_data['customer'])
                })
                line = order_lines(j_data['line_items'], order)

                # i now have to add the lines id
                http.request.env['sale.order'].sudo().write({
                    'line_id': line.id
                })
                return 'Success'
            except:
                return {
                    'error': 'An Error Occurred while creating sales order'}
        else:
            return {
                'error': 'Required Data values not Found'}

    # Demo endpoint to test the inventory API
    @http.route('/shopify/order/post', type='http', auth="public", website=True, methods=["POST"], csrf=False)
    def inventory_post(self):
        data = yaml.load(request.httprequest.data)
        print(data)
