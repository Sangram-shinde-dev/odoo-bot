{
    'name': 'odoo AI',
    'sequence': 1,
    'version': '16.0.1.0.0',
    'category': 'Communication',
    'summary': 'AI Chatbot Integration for Odoo with odooBot',
    'description': 'This module integrates odooBot, an AI-based chatbot, into Odoo.',
    'author': 'Trinesis-Sangram',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
        'portal',  # If the bot is considered a portal user
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_ai_views.xml',
        'data/odoo_bot_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
