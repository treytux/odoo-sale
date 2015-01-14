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


class SaleReport(models.Model):
    _inherit = 'sale.report'
    _auto = False

    margin = fields.Float(
        'Margin', readonly=True)
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Partner state',
        readonly=True)

    def _select(self):
        select_str = super(SaleReport, self)._select()
        return '%s %s' % (
            select_str,
            ',l.margin as margin'
            ',rp.state_id as state_id')

    def _from(self):
        from_str = super(SaleReport, self)._from()
        return '%s %s' % (
            from_str,
            'left join res_partner rp on (rp.id=s.partner_id)')

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        return '%s %s' % (
            group_by_str,
            ',l.margin'
            ',rp.state_id')
        return group_by_str
