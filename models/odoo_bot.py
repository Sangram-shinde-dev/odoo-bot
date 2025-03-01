from odoo import models, fields, api

class odooBot(models.Model):
    _name = 'odoo.bot'
    _description = 'odoo AI Bot'
    _inherit = 'mail.channel'

    @api.model
    def create_private_channel(self, user_id):
        # Get the odooBot system user and the user who initiated the conversation
        odoobot_user = self.env.ref('your_module.base_user_odoo_bot_new')
        user = self.env['res.users'].browse(user_id)

        # Check if a private channel already exists for the user and odooBot
        existing_channel = self.env['mail.channel'].search([
            ('is_private', '=', True),
            ('channel_type', '=', 'chat'),
            ('name', '=', f"Private Chat with {odoobot_user.name}")
        ], limit=1)

        if existing_channel:
            return existing_channel  # Return the existing channel if found

        # Create a new private channel between the user and odooBot
        channel = self.env['mail.channel'].create({
            'name': f"Private Chat with {odoobot_user.name}",
            'is_private': True,
            'channel_type': 'chat',
        })

        # Subscribe both odooBot and the user to the channel
        channel.message_subscribe([odoobot_user.partner_id.id, user.partner_id.id])

        # Return the private channel object
        return channel
