# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from openerp import models, fields, api, exceptions, _


class PrintInvoiceReport(models.TransientModel):
    _name = 'wiz.print_invoice_report'

    # Obtiene los informes de factura
    def _get_default_report(self):
        report_ids = self.env['ir.actions.report.xml'].search(
            [('model', '=', 'account.invoice')])

        if report_ids:
            return report_ids[0]
        else:
            raise osv.except_osv(
                'Atencion',
                'No hay ningun informe disponible para la factura.')

    report_id = fields.Many2one(
        comodel_name='ir.actions.report.xml',
        string='Report',
        domain=[('model', '=', 'account.invoice')],
        default=_get_default_report,
        required=True)

    @api.multi
    def button_print_invoice(self):

        # Buscar el id del pedido
        order_ids = self.env.context['active_ids']
        orders = self.env['sale.order'].browse(order_ids)

        # Buscar facturas asociadas a los pedidos
        invoice_ids = [
            i.id for o in orders for i in o.invoice_ids if i.state != 'cancel']

        # Si no hay factura, mostrar msg
        if not invoice_ids:
            raise exceptions.Warning(_('MENSAJE'))

        # Si hay factura/s, lanzar el report con los ids de la/s factura/s
        datas = {'ids': invoice_ids}

        # Lanzar informe
        return {
            'type': 'ir.actions.report.xml',
            'report_name': self.report_id.report_name,
            'datas': datas,
        }


