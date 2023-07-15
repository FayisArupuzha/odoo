from odoo import models, fields, api

class Student(models.Model):
    _inherit = "product.template"
    
    school_check_product=fields.Boolean()
    value_product = fields.Integer(string="Value")
    
    
    def id_button(self):
        for each in self.env['product.template'].search([]):
            each.value_product = each.id