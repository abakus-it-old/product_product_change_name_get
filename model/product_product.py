from openerp import models, api

class product_product_brand(models.Model):
    _inherit = 'product.product'

    #Redefines the name_get method from product.product.
    #It is the same method's body but it includes the brand.
    @api.multi
    def name_get(self):
        result = []
        for product in self:
            result.append((product.id, product.name_get_full()))
        return result

    @api.one
    def name_get_full(self):
        fullName = ''
        
        if self.product_brand_id:
            fullName += self.product_brand_id.name + ' - '
        
        fullName += self.name
        
        if self.default_code:
            fullName += ' [{}]'.format(self.default_code)

        return fullName
