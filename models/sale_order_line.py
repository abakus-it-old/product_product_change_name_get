from openerp import models, api

class sale_order_line(models.Model):
    _inherit='sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(sale_order_line, self).product_id_change()

        if self.product_id:
            vals = {}
            if self.product_id.description_sale:
                vals['name'] = self.product_id.description_sale
            elif self.product_id.description:
                vals['name'] = self.product_id.description
            else:
                vals['name'] = self.product_id.name

            self.update(vals)

        return result
        
sale_order_line()