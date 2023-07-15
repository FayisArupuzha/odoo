{
    'name': 'Odoo 16 Report_invoice_Alsi',
    'author': 'Fayis',
    'category': 'Invoice',
    'version': '16.0.0.1',
    'description': """ """,
    'summary': 'new filed creation in odoo.sale',
    # 'sequence': 11,
    # 'website': 'https://www.odoomates.tech',
    'depends': ['account','sale','invoice_reports'],
    'license': 'LGPL-3',
    'data': [
        "reports/header_footer_alsi.xml",
        "reports/invoice_alsi_main.xml",
        # "reports/papper_format.xml",
        "reports/new_papper_format.xml",
        
        
    ],
}    