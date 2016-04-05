from openerp import models, fields, api

class product_product_brand(models.Model):
    _inherit = 'product.product'

    #Redefines the name_get method from product.product.
    #It is the same method's body but it includes the brand.
    @api.multi
    def name_get(self):
        result = []
        for product in self:
            result.append((product.id, "%s" % (self.name_get_full(product))))
        return result

    @api.model
    def name_get_full(self, product):
        name = product.name
        if product.product_brand_id:
            name = product.product_brand_id.name + " - " + name
        if product.code:
            name = product.code + " - " + name
        return name

    @api.model
    def name_get_no_code(self, product):
        name = product.name
        if product.product_brand_id:
            name = product.product_brand_id.name + " - " + name
        return name