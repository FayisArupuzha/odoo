from odoo import models,fields,api
from odoo.http import request
from odoo import http, _


class ProductHosting(models.Model):
    _name = "product.hosting.web"

    software = fields.Char(string="Software")
    price = fields.Char(string="Price")
    description = fields.Text("Description")
    publication = fields.Boolean(string="publication")


    # @http.route(['/event/init_barcode_interface'], type='json', auth="user")
    def website(self):
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/OdooServices',
            'target': 'self',  # Open the page in the same window
        }
        