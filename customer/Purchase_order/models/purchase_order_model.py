from odoo import models, fields


class Purchase_order(models.Model):
    _name = "customer.purchase.order"
    _rec_name = "product_name"
    product_name = fields.Char(string="Product Name")
    prise = fields.Char(string="Price")
    # name = fields.Char(string="name")