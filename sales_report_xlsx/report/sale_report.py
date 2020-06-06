from odoo import models


class saleOrderXlsx(models.AbstractModel):
    _name = 'report.sales_report_xlsx.report_sale_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, saleOrder):
        sheet = workbook.add_worksheet('Sales Orders')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Quotation name', bold)
        sheet.write(0, 1, 'Order Date', bold)
        sheet.write(0, 2, 'Products', bold)
        sheet.write(0, 3, 'Customer', bold)
        sheet.write(0, 4, 'Sales Person', bold)
        sheet.write(0, 5, 'Company', bold)
        sheet.write(0, 6, 'Total', bold)
        line = 2
        for obj in saleOrder:
            sheet.write(line, 0, obj.name)
            sheet.write(line, 1, obj.date_order)
            products = []
            for order in obj.order_line:
                products.append(order.product_id.name + ' - ' + str(order.product_uom_qty))
                sheet.write(line, 2, ", ".join(products))
            sheet.write(line, 3, obj.partner_id.name)
            sheet.write(line, 4, obj.user_id.name)
            sheet.write(line, 5, obj.company_id.name)
            sheet.write(line, 6, obj.amount_total)

            line = line + 1
