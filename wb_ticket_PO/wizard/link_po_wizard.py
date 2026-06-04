# -- coding: utf-8 --
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Wan Buffer Solution (<https://wanbuffer.com/>).
#
#    For Module Support : info@wanbuffer.com  or Call : +91 9638442270
#
##############################################################################

from odoo import models, fields, _
from odoo.exceptions import UserError

class LinkPOWizard(models.TransientModel):
    _name = 'wb.link.po.wizard'
    _description = 'Wizard to Link Existing Purchase Orders'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True, readonly=True)
    purchase_order_ids = fields.Many2many(
        'purchase.order', 
        string='Purchase Orders', 
        required=True,
        domain="[('helpdesk_ticket_id', '=', False), ('state', '!=', 'cancel')]"
    )

    def action_link_po(self):
        """
        Links the selected purchase orders to the ticket.
        Also explicitly checks for prior linking to be safe.
        """
        self.ensure_one()
        
        for po in self.purchase_order_ids:
            if po.helpdesk_ticket_id:
                 raise UserError(_("Purchase Order %s is already linked to ticket %s.") % (po.name, po.helpdesk_ticket_id.name))
        
        # Link the POs
        self.purchase_order_ids.write({'helpdesk_ticket_id': self.ticket_id.id})
        
        # Trigger stage move if needed (though 'write' on PO triggers it via override usually)
        # But calling it here explicitly ensures immediate UI feedback if write override uses different logic
        self.ticket_id._move_to_po_generated_stage()
        
        return {'type': 'ir.actions.act_window_close'}
