# -- coding: utf-8 --
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Wan Buffer Solution (<https://wanbuffer.com/>).
#
#    For Module Support : info@wanbuffer.com  or Call : +91 9638442270
#
##############################################################################

from odoo import models, fields, api, _
from markupsafe import Markup

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Originating Ticket',
        readonly=True,
        help="Support Ticket that generated this Purchase Order."
    )

    def message_post(self, **kwargs):
        """
        Override to sync chatter messages from Purchase Order to the linked Helpdesk Ticket.
        Wraps content in Markup to prevent HTML escaping.
        """
        message = super().message_post(**kwargs)
        for order in self:
            if order.helpdesk_ticket_id:
                body = kwargs.get('body', '')
                tracking_value_ids = kwargs.get('tracking_value_ids', [])
                
                # Format tracking values if present
                tracking_msg = ""
                if tracking_value_ids:
                    changes = []
                    for cmd in tracking_value_ids:
                        # tracking_value_ids is typically a list of (0, 0, values) tuples
                        if isinstance(cmd, (tuple, list)) and len(cmd) == 3 and cmd[0] == 0:
                            vals = cmd[2]
                            field_desc = vals.get('field_desc', 'Field')
                            old_val = vals.get('old_value_char') or vals.get('old_value_integer') or vals.get('old_value_float') or ''
                            new_val = vals.get('new_value_char') or vals.get('new_value_integer') or vals.get('new_value_float') or ''
                            
                            # Handle empty values for display
                            if not old_val: old_val = _('None')
                            if not new_val: new_val = _('None')
                            
                            changes.append(f"<li>{field_desc}: {old_val} &rarr; {new_val}</li>")
                    
                    if changes:
                        tracking_msg = "<ul>" + "".join(changes) + "</ul>"

                # Prepare safe HTML prefix
                prefix = Markup(_("<strong>Log from %s:</strong><br/>")) % order._get_html_link()
                
                # Combine: Prefix + Body + Tracking
                # We use Markup() for tracking_msg to ensure the <ul>/<li> tags are rendered
                parts = [prefix]
                if body:
                    parts.append(Markup(body))
                if tracking_msg:
                    parts.append(Markup(tracking_msg))
                
                if len(parts) > 1: # If we have body OR tracking (prefix is always there)
                    new_body = Markup("").join(parts)
                    
                    order.helpdesk_ticket_id.message_post(
                        body=new_body,
                        subject=kwargs.get('subject'),
                        message_type=kwargs.get('message_type', 'notification'),
                        subtype_xmlid=kwargs.get('subtype_xmlid'),
                        subtype_id=kwargs.get('subtype_id'),
                        attachment_ids=kwargs.get('attachment_ids'),
                    )
        return message

    @api.model_create_multi
    def create(self, vals_list):
        """Override to log creation on linked ticket and move stage."""
        orders = super().create(vals_list)
        for order in orders:
            if order.helpdesk_ticket_id:
                order.helpdesk_ticket_id._move_to_po_generated_stage()
                msg = Markup(_("Purchase Order created: %s")) % order._get_html_link()
                order.helpdesk_ticket_id.message_post(body=msg, subtype_xmlid='mail.mt_note')
        return orders

    def write(self, vals):
        """Override to log linking actions on linked ticket."""
        res = super().write(vals)
        if 'helpdesk_ticket_id' in vals and vals['helpdesk_ticket_id']:
            for order in self:
                if order.helpdesk_ticket_id:
                    order.helpdesk_ticket_id._move_to_po_generated_stage()
                    msg = Markup(_("Purchase Order linked: %s")) % order._get_html_link()
                    order.helpdesk_ticket_id.message_post(body=msg, subtype_xmlid='mail.mt_note')
        return res

    def button_cancel(self):
        """Override to log cancellation on linked ticket."""
        res = super().button_cancel()
        for order in self:
            if order.helpdesk_ticket_id:
                msg = Markup(_("Purchase Order cancelled: %s")) % order._get_html_link()
                order.helpdesk_ticket_id.message_post(body=msg, subtype_xmlid='mail.mt_note')
        return res

    def unlink(self):
        """Override to log deletion on linked ticket."""
        for order in self:
            if order.helpdesk_ticket_id:
                msg = Markup(_("Purchase Order deleted: %s")) % order.name
                order.helpdesk_ticket_id.message_post(body=msg, subtype_xmlid='mail.mt_note')
        return super().unlink()
