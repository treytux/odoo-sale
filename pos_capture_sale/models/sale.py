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
from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pos_order_id = fields.Many2one(
        comodel_name='pos.order',
        string='Pos Order',
        readonly=True,
        help="Pos Order relationated.")

    # Anade valor al campo estado de pedido de ventas
    def __init__(self, pool, cr):
        super(SaleOrder, self).__init__(pool, cr)

        option = ('manage_from_pos', 'Manage from PoS')
        type_selection = self._columns['state'].selection

        if option not in type_selection:
            type_selection.append(option)
