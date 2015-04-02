from openerp.osv import fields, osv

class sale_order_line(osv.osv):
    _inherit='sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
        uom=False, qty_uos=0, uos=False, name='', partner_id=False,
        lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        
        result = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, context)
        
        product_obj = self.pool.get('product.product')
        partner_obj = self.pool.get('res.partner')
        partner = partner_obj.browse(cr, uid, partner_id)
        context_partner = {'lang': partner.lang, 'partner_id': partner_id}
        product_obj = product_obj.browse(cr, uid, product, context=context_partner)
        
        if not flag:
            result['value']['name'] = self.pool.get('product.product').name_get_without_reference(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['value']['name'] += '\n'+product_obj.description_sale

        return result

sale_order_line()