# -*- coding: utf-8 -*-

from openerp import models, api

class sale_order_line(models.Model):
    _inherit='sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(sale_order_line, self).product_id_change()
        
        if self.product_id:
            vals = {}
            
            #get the product in partner lang
            partner = self.order_id.partner_id
            if partner.lang:
                product = self.product_id.with_context(lang=partner.lang)
            else:
                product = self.product_id
            
            #select the good description
            if product.description_sale:
                vals['name'] = product.description_sale
            elif product.description:
                vals['name'] = product.description
            else:
                vals['name'] = product.name

            self.update(vals)

        return result
        
sale_order_line()