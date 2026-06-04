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
from odoo.exceptions import UserError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    purchase_order_ids = fields.One2many(
        'purchase.order',
        'helpdesk_ticket_id',
        string='Purchase Orders'
    )
    po_count = fields.Integer(compute='_compute_po_count', string="Purchase Orders")

    @api.depends('purchase_order_ids')
    def _compute_po_count(self):
        for ticket in self:
            ticket.po_count = len(ticket.purchase_order_ids)

    def action_create_purchase_order(self):
        """Action to trigger creation of a new PO linked to this ticket."""
        self.ensure_one()
        return {
            'name': _('Create Purchase Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'context': {
                'default_helpdesk_ticket_id': self.id,
                'default_origin': self.name,
                'default_partner_id': self.partner_id.id, 
            },
        }

    def action_view_purchase_orders(self):
        """Action to view the list of linked Purchase Orders."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
        action['context'] = {'default_helpdesk_ticket_id': self.id}
        return action

    def action_link_existing_po(self):
        self.ensure_one()
        return {
            'name': _('Link Existing Purchase Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'wb.link.po.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_ticket_id': self.id},
        }

    def _move_to_po_generated_stage(self):
        """Finds a stage named 'PO Generated' and moves the ticket there."""
        stage = self.env['helpdesk.stage'].search([
            ('name', '=', 'PO Generated'),
            '|', ('team_ids', '=', False), ('team_ids', 'in', [self.team_id.id])
        ], limit=1)
        
        if stage:
            # Check if stage is linked to team. If not, link and resort.
            if self.team_id and stage.team_ids and self.team_id not in stage.team_ids:
                 # Add stage to team
                 current_stages = self.team_id.stage_ids | stage
                 # Sort and write
                 sorted_stages = current_stages.sorted(key=lambda s: s.sequence)
                 self.team_id.write({'stage_ids': [(6, 0, sorted_stages.ids)]})
            
            elif self.team_id and not stage.team_ids:
                 # Similar logic if it was global
                 current_stages = self.team_id.stage_ids | stage
                 sorted_stages = current_stages.sorted(key=lambda s: s.sequence)
                 self.team_id.write({'stage_ids': [(6, 0, sorted_stages.ids)]})

            self.write({'stage_id': stage.id})
