from odoo import models, fields,api

class Purchase_order_custome(models.Model):
    _inherit = 'purchase.order'
    
    sale_id = fields.Many2many('sale.order', string="sale")
    school_id = fields.Many2one('sale.school',string="Sale School")