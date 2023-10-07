from odoo import http
from odoo.http import request

class OnlineEvent(http.Controller):
    """ set the route in website search the values in events """

    @http.route('/OdooServices', type='http', auth='public', website=True)
    def custom_website(self):
        enquiry_id = request.env['product.hosting.web'].search([('publication','=',True)])
        return request.render('web_site_hosting.product_enquiry_page', {'enquiry': enquiry_id,})
    
    @http.route('/OdooServices/form', type='http', auth='public', website=True)
    def register_new(self):
        enquiry_id = request.env['product.hosting.web'].search([])

        return request.render('web_site_hosting.new_form_template', {'enquiry': enquiry_id,})
    
    @http.route('/enquiry-form/submit', type='http', auth='public', website=True, csrf=False)
    def submit_enquiry_form(self, **post):
        # Create a CRM lead with the submitted data
        Lead = request.env['crm.lead']
        lead_data = {
            'name': post.get('name'),
            # 'partner_id': post.get('company'),
            'phone': post.get('phone'),
            'email_from': post.get('email'),

        }
        new_lead = Lead.create(lead_data)

        # Redirect to a thank you page or a confirmation message
        return request.render('web_site_hosting.contacts',)

