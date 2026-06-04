{
    "name": "Helpdesk Ticket to Purchase Order",
    "version": "18.0.1.0.0",
    "summary": "Link Support Tickets to Purchase Orders",
    "description": """Enhance your procurement workflow by seamlessly connecting Helpdesk Tickets with Purchase Orders.
            This module streamlines the entire process from ticket creation to purchase order management, ensuring perfect 
            traceability and better team collaboration. Users can create new purchase orders or link existing ones directly 
            from helpdesk tickets with just a few clicks. All communication and status changes are automatically synchronized 
            between tickets and purchase orders, keeping your support and procurement teams in perfect sync. The module features 
            intelligent stage transitions, comprehensive audit trails, smart button access, and pre-populated forms for faster 
            order creation. Designed for both support staff and procurement teams, it simplifies relationship management, 
            boosts productivity, and ensures seamless workflow integration across your Odoo instance.
            """,
    "category": "Helpdesk",
    "author": "Wan Buffer Services",
    "depends": ["helpdesk", "purchase", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "data/helpdesk_data.xml",
        "views/helpdesk_ticket_views.xml",
        "views/purchase_order_views.xml",
        "wizard/link_po_wizard_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "images": ["static/description/background.png", ],
    "installable": True,
    "application": False,
    "website": "https://wanbuffer.com",
    "maintainer": "Wan Buffer Services",
    "support": "info@wanbuffer.com",
    "license": "LGPL-3",
}
