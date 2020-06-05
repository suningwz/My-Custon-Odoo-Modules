from odoo import models


class saleOrderXlsx(models.AbstractModel):
    _name = 'report.sales_report_xlsx.report_sale_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, saleOrder):
        for obj in saleOrder:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, 'Quotation name', bold)
            sheet.write(2, 0, obj.name)
            sheet.write(0, 1, 'Order Date', bold)
            sheet.write(2, 1, obj.date_order)
