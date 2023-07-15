from odoo import models, fields, api
import json as json 


class demo_wizard(models.TransientModel):
    _name = 'school.wizard.model'
    _description = 'Test Model Wizard'
    
    products=fields.Many2one('product.product' , string="Product")
    check_list = fields.Boolean(default=True,  string='Check List')
    check_product = fields.Boolean(string='Check product',)
    link_field = fields.Many2one("sale.school",string ="Id field")
    wizard_somany_field = fields.Many2many('product.product')
            
    def ok_button(self):
        if self.check_list == True:
            if self.link_field:
                for each in self.link_field.school_line_ids:
                    if each.product_id.id ==self.products.id:
                        each.unlink() 
                                    
    @api.onchange('check_list')
    def product_compute_select(self):
        self.check_product =True
        if self.link_field:
            product_list = []
            for each in self.link_field.school_line_ids:
                product_list.append(each.product_id.id)
            return {
            'domain': {
                'products': [('id', 'in', product_list)]
                }
            }
                
          
                    
        