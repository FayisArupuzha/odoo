from odoo import models, fields

class Sale_order(models.Model):
    _inherit ="sale.order"
    
    order_user = fields.Char(string='User')
    order_users = fields.Many2one('res.users',string='Users',default=lambda self: self.env.user)
    link_field =fields.Many2one('stock.picking', string='Inventory')
    

   
# class SaleOrderLine(models.Model):

#      _inherit = 'sale.order.line'

#      user = fields.Many2one('res.users',string='User')

