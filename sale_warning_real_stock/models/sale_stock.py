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
from openerp import models, api, exceptions, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        product_obj = self.env['product.product']
        warning_msgs = ''
        if product and res['value']['product_uos_qty']:
            product = product_obj.browse(product)
            if res['value']['product_uos_qty'] > product.qty_available:
                warn_msg = _('You plan to sell %.2f %s but you only have %.2f %s '
                         'available !\nThe real stock is %.2f %s. '
                         '(without reservations)') % \
                    (qty, product.uom_id.name,
                        max(0, product.virtual_available), product.uom_id.name,
                        max(0, product.qty_available), product.uom_id.name)
                warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"
        if warning_msgs:
            raise exceptions.Warning(warning_msgs)
        return res
