from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class sale_order_line(models.Model):
    _inherit='sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(sale_order_line, self).product_id_change()

        if self.product_id:
            _logger.debug("Product: %s", self.product_id)
            # Get the partner in order to have the correct language
            lang = self.order_id.partner_id.lang
            vals = {}
            if self.product_id.description_sale:
                vals['name'] = self.with_context(lang=lang).product_id.description_sale
            elif self.product_id.description:
                vals['name'] = self.with_context(lang=lang).product_id.description
            else:
                vals['name'] = self.with_context(lang=lang).product_id.name

            self.update(vals)

        return result
        
sale_order_line()