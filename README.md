# Helpdesk Ticket to Purchase Order

> Turn support tickets into procurement actions — create or link a Purchase Order straight from a Helpdesk Ticket, with synced chatter, stage transitions and smart-button navigation.

Repository: https://github.com/Wan-Buffer-Services/helpdesk-to-PO.git
Odoo module: `wb_ticket_PO`

## Overview

**Helpdesk Ticket to Purchase Order** connects the Helpdesk and Purchase apps so the moment a support ticket requires procurement (parts to replace, items to source, warranty restocks…) the procurement step happens right from the ticket. Either spin up a new PO with the customer/vendor context already filled in, or link an existing PO and keep the audit trail intact.

Both sides stay in sync: chatter, status changes and ticket stages move together so support and procurement teams work off the same record.

## Key Features

- **Create new Purchase Order** from a Helpdesk Ticket (pre-populated form for faster order creation).
- **Link existing Purchase Order** via the *Link PO* wizard.
- **Smart buttons** on the ticket → PO and PO → ticket for quick navigation.
- **Bi-directional chatter sync**: messages and status changes are mirrored between ticket and PO.
- **Intelligent stage transitions** — tickets advance to a dedicated procurement stage when a PO is created/linked (set up by `data/helpdesk_data.xml`).
- **Comprehensive audit trail** linking every PO to the originating ticket.
- **Post-install hook** seeds the new stage and configuration automatically.
- **Stock-aware** (depends on `stock`) so receipts flow naturally from the PO.

## Module Info

| | |
|---|---|
| Module | `wb_ticket_PO` |
| Display name | Helpdesk Ticket to Purchase Order |
| Category | Helpdesk |
| Version | 18.0.1.0.0 |
| License | LGPL-3 |
| Depends on | `helpdesk`, `purchase`, `stock` |
| Author / Support | Wan Buffer Services — info@wanbuffer.com |

## Installation

1. Clone the repository into your Odoo addons path:
   ```bash
   git clone https://github.com/Wan-Buffer-Services/helpdesk-to-PO.git
   ```
2. Update the apps list and install **Helpdesk Ticket to Purchase Order**, or via CLI:
   ```bash
   odoo-bin -c <conf> -d <db> -i wb_ticket_PO
   ```
   The `post_init_hook` runs on first install to add the procurement stage and seed data.

## Usage

1. Open a Helpdesk Ticket that needs procurement.
2. Click **Create PO** to spin up a Purchase Order with vendor/product/customer context pre-filled, or **Link PO** to attach an existing one via the wizard.
3. The ticket advances to the procurement stage and a smart button to the PO appears.
4. From the Purchase Order side, a smart button takes you back to the ticket. Messages on either record sync to the other via chatter.

## Support

Wan Buffer Services — https://wanbuffer.com · info@wanbuffer.com · +91 9638442270
