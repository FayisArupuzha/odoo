{
    'name': 'Odoo 16 school',
    'author': 'Odoo Mates',
    'category': 'Sale',
    'version': '16.0.0.1',
    'description': """ """,
    'summary': 'new filed creation in odoo.sale.school',
    # 'sequence': 11,
    # 'website': 'https://www.odoomates.tech',
    'depends': ['sale','purchase'],
    'license': 'LGPL-3',
    'data': [
        'wizard/wizard-demo.xml',
        'views/school.xml',
        'views/custome_purchase_order.xml',
        'views/custome_school_product.xml',
        'views/sale_custome_sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

    ],
}    