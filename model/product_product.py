from openerp import SUPERUSER_ID
from openerp import models, fields, api

class product_product_brand(models.Model):
    _inherit = 'product.product'

    #Redifines the name_get method from product.product.
    #It is the same method's body but it includes the brand.
    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get(d):
            name = d.get('name','')
            brand = d.get('brand','')
            code = context.get('display_default_code', True) and d.get('default_code',False) or False
            if code:
                if brand:
                    name = '%s - %s [%s]' % (brand.upper(),name,code)
                else:
                    name = '%s [%s]' % (name,code)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)
        if partner_id:
            partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id, context=context).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights(cr, user, "read")
        self.check_access_rule(cr, user, ids, "read", context=context)

        result = []
                
        for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
            variant = ", ".join([v.name for v in product.attribute_value_ids])
            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                sellers = filter(lambda x: x.name.id in partner_ids, product.seller_ids)
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'brand': product.product_brand_id.name,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    result.append(_name_get(mydict))
            else:
                mydict = {
                          'id': product.id,
                          'brand': product.product_brand_id.name,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result

    def name_get_without_reference(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get_without_reference(d):
            name = d.get('name','')
            brand = d.get('brand','')
            if brand:
                name = '%s - %s' % (brand.upper(),name)
            else:
                name = '%s' % (name)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)
        if partner_id:
            partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id, context=context).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights(cr, user, "read")
        self.check_access_rule(cr, user, ids, "read", context=context)

        result = []
                
        for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
            variant = ", ".join([v.name for v in product.attribute_value_ids])
            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                sellers = filter(lambda x: x.name.id in partner_ids, product.seller_ids)
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'brand': product.product_brand_id.name,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    result.append(_name_get_without_reference(mydict))
            else:
                mydict = {
                          'id': product.id,
                          'brand': product.product_brand_id.name,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get_without_reference(mydict))
        return result