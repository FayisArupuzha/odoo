from odoo import models, fields, api

class Student(models.Model):
    _name = "sale.school"


    class_name = fields.Char(string='Class')
    student_class = fields.Char(string='Student')
    total_mark= fields.Integer(string='Total Mark')
    count = fields.Integer(string="Count", default=1)
    change_mark = fields.Integer(string="Changed Mark")
    total_line = fields.Integer(string="Total Line", compute="compute_total_count_form")
    vender = fields.Many2one('res.partner', string="Vender")
    purchase_check = fields.Many2many('purchase.order' , compute='compute_purchase_check')
    # Page line    
    school_line_ids = fields.One2many('sale.school.line', 'sale_id', string="Sale School Line")
    purchase_order = fields.Many2one('purchase.order', string= "Purchase Order")
    purchase_count = fields.Integer(string="Count", compute="compute_total_count_Purchase" ) 
    somany_product = fields.Many2many('product.product', string='Product List')    
    link_field_product_template = fields.Many2one('product.template', string="link field product")
    application_no = fields.Char(string='Application No.', required=True, readonly=True, default=lambda self: ('New'))
    save_bool= fields.Boolean()
    order_users = fields.Many2one('res.users',string='Users',default=lambda self: self.env.user if self.env.user.has_group('school.overtime_manager_access_school') else False)

    #new code
    # vender = fields.Many2one('res.partner', string="Vender")
    # count_purchase_order = fields.Integer()
    
    # @api.model
    # def create(self, vals):
    #     vals['application_no'] = self.env['ir.sequence'].next_by_code('sequence.school')
    #     return super('sale.school', self).create(vals)
    
    
    # @api.model
    # def create(self, vals):
    #     if vals.get('application_no', 'New') == 'New' and vals.get('save_bool',) :
    #         sequence_code = 'sequence.school123'
    #         field_value = vals.get('student_class')
    #         if field_value:
    #             sequence_code = field_value[0:3] + '\\'
    #         vals['application_no'] = sequence_code + self.env['ir.sequence'].next_by_code('sequence.school123') or 'New'

    #     res = super(Student, self).create(vals)
    #     return res
    
    @api.model
    def create(self, vals):
        res = super(Student, self).create(vals)
        current_user =self.env.user
        if current_user.has_group('school.overtime_manager_access_school'):
            vals['order_users'] = self.env.user.id
            new_res = super(Student, self).create(vals)
            return new_res
        else:
            return res

    
    
    
    # def custom_options_initializer(self, report, options, previous_options=None):
    #     # Remove multi-currency columns if needed
    #     super()._custom_options_initializer(report, options, previous_options=previous_options)
    #     if not self.user_has_groups('base.group_multi_currency'):
    #         options['columns'] = [
    #             column for column in options['columns']
    #             if column['expression_label'] != 'amount_currency'
    #         ]
                
    def save_create(self):
        if self.application_no == 'New' :
            field_value = self.student_class          
            
            sequence_code = field_value[0:3] + '\\'
            sequence_code1 = '\\' + field_value[-2:]
            
            new_field_save = sequence_code + self.env['ir.sequence'].next_by_code('sequence.school123') + sequence_code1 or 'New'
            self.application_no = new_field_save
        
    
    def action_back(self):
        pass
    
    
    
    
    @api.onchange('count','total_mark')
    def onchange_school_line_ids(self):
        school_lines = []
        split_mark = self.total_mark / self.count
        for rec in range(self.count):
            new_line = self.env['sale.school.line'].create({
                'mark' : split_mark
            })
            school_lines.append(new_line.id)
            
        self.school_line_ids = [(6, 0, school_lines)]
    
   
    @api.onchange('school_line_ids',)
    def change_marks(self):
        total= self.total_mark
        sum1=0    
        for line in self.school_line_ids:
    
            sum1 += line.mark
        self.change_mark =  sum1 - total 
        
            
    def compute_total_count_form(self):
        count_line = 0
        sale_school = self.env['sale.school'].search([])
        for rec in sale_school.school_line_ids:
            count_line+=1
        sale_school.total_line = count_line
            
    def Purchase_list(self):
        self.ensure_one()
        return {
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order',
                'view_mode': 'tree,form',
                'res_model': 'purchase.order',
                # 'domain': [('id', '=', self.purchase_order.id)],
                # 'context': "{'create': False}"
            }    
   
            
            
    def Purchase_create(self):
        purchase_line= []
        for line in self.school_line_ids:
            purchase_line.append((0, 0,{
                'product_qty': line.quantity,
                'price_unit' : line.price,
                'name' : line.product_dis,
                'product_id' : line.product_id.id,
            }))
            rec = self.env['purchase.order'].create({
                    'partner_id': self.vender.id,
                    'order_line': purchase_line,
                    'school_id' : self.id,
                })
            # records = self.env['purchase.order'].search([('school_id','=',self.id)])
            # self.write({
            #     "purchase_check":[(6,0,records.ids)]
            #     })
            
    # @api.depends('sale.school')
    def compute_purchase_check(self):
        self.ensure_one()
        records = self.env['purchase.order'].search([('school_id','=',self.id)])
        self.write({
                "purchase_check":[(6,0,records.ids)]
                })
        
        
        
    
    @api.depends('purchase_order')
    def compute_total_count_Purchase(self):
        for record in self:
            count_line = self.env['purchase.order.line'].search_count([('order_id', '=', record.purchase_order.id)])
        self.purchase_count = count_line
    
    def check_order(self):
        self.ensure_one()
        return {
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order',
                'view_mode': 'tree,form',
                'res_model': 'purchase.order',
                'domain': [('school_id', '=', self.id)],
        }
        
    def register_payment(self):
        
        list_value = []
        for each in self.school_line_ids:
                list_value.append(each.product_id.id)
        
        return {
            'name' : "create wizard",
            'type' :  'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode': 'form',
            'res_model': 'school.wizard.model',
            'target' : 'new',
            'context' : {
                'default_link_field' : self.id,
                'default_wizard_somany_field' : [(4, x)for x in list_value]
                # 'default_products' : self.school_line_ids.product_id.id
            }
            
        }
    def product_button_list(self):
        school_lines = []
        for line in reversed(self.somany_product):    
            new_line = self.env['sale.school.line'].create({
                        'product_list' : line
                    })
            school_lines.append(new_line.id)
                
            self.school_line_ids = [(6, 0, school_lines)]    

    def button_for_value(self):
        record = self.env['product.template'].search([])
        record.value_product = 20
        for line in self.somany_product:
            search = record.search([('id','=',line.id)])
            search.value_product = 30
                
                    
                
            
            
            
        
            
       
class StudentLine(models.Model):
    _name = 'sale.school.line'
    sale_id = fields.Many2one(
        "sale.school",
        string="School",
    )
    
    mark = fields.Float(string="Mark")
    subject = fields.Char(string='Subject')
    #new code
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="price")
    product_dis = fields.Text(string="Product Discripton")
    product_id = fields.Many2one('product.product', string="Product",domain="[('school_check_product', '=', True)]")
    product_list = fields.Many2many('product.product', string= 'Product list')
    # school_check_product_id=fields.Many2one('product.template',)
    
    # # @api.onchange('subject')
    # def product_check_compute_select(self):
    #     self.school_check_product_id=1
    #     search_product = self.env['product.template'].search([])
    #     product_list = []
    #     for rec in search_product:
    #         if rec.school_check_product == True:
    #             product_list.append(rec.id)
    
    #     return {
    #         'domain': {
    #             'product_id': [('id', 'in', product_list)]
    #             }
    #         }                   

    
    #             # 'domain': [('school_id', '=', self.id)],


    
