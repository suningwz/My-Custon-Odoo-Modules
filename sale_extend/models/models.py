# -*- coding: utf-8 -*-

from odoo import models
import requests


class sale_extend(models.Model):
    _inherit = 'sale.order'
    _description = 'Extension of sale order'

    def send_api(self):
        if self.state == 'sale':
            data = {
                # shipment details
                "shipments": [
                    {
                        "client": self.partner_id.name,  # client name
                        "name": self.user_id,  # sales person’s name
                        "order": self.client_order_ref,  # client order number
                        # product description (not name)
                        "products_desc": self.order_line.product_id,
                        "order_date": self.date_order,  # ISO Format
                        "total_amount": self.amount_total,  # in INR
                        "add": self.partner_id.street,  # client address
                        "city": self.partner_id.city,
                        "state": self.partner_id.state_id.name,
                        "country": self.partner_id.country_id.name,
                        "phone": self.partner_id.phone,
                        "pin": self.partner_id.zip,
                        # optional
                        "return_add": "",
                        "return_city": "",
                        "return_country": "",
                        "return_name": "",
                        "return_phone": "",
                        "return_pin": "",
                        "return_state": "",
                        # optional
                        "supplier": "Kangaroo (India) Pvt Ltd",
                        # optional  Extra parameters that need to be send with packages. This should be unicoded dictionary
                        "extra_parameters": "",
                        "shipment_width": "",  # optional width of shipment
                        "shipment_height": "",  # optional  height of shipment
                        "weight": "650.0 gm",  # required
                        "quantity": 1,  # quantity of goods, positive integer
                        "seller_inv": "invoice number",
                        "seller_inv_date": "YYYYMMDDTHH:MM:SS+05:30",  # ISO format
                        "seller_name": "seller name",  # name of seller
                        "seller_add": "seller add",  # seller address
                        "seller_cst": "seller cst",  # seller cst no
                        "seller_tin": "seller tin",  # seller tin no
                        # extra(optional)
                        "consignee_tin": "consignee tin",  # consignee tin no
                        "commodity_value": "commodity value",  # commodity value
                        "tax_value": "tax value",  # tax value
                        # Sale Tax Form Acknowledge No.
                        "sales_tax_form_ack_no": "",
                        "category_of_goods": "",
                        "seller_gst_tin": "seller_gst_tin",
                        "client_gst_tin": "client_gst_tin",
                        "consignee_gst_tin": "consignee_gst_tin",
                        "hsn_code": "hsn_code",
                        "invoice_reference": "invoice_reference"  # unique invoice reference number
                    }]
            }
            # requests.post("", json=data)
            print(data)
