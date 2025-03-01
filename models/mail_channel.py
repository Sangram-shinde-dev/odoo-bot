import logging
import requests  # Used to make HTTP requests to the API
from odoo import api, models, _

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    API_KEY = 'Your-APi-Key'  # Update with your actual Gemini API key
    GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

    @api.model
    def create(self, vals):
        """Intercept incoming chat messages and trigger odooBot's response once."""
        message = super(MailMessage, self).create(vals)

        # Ensure the message is from a channel (i.e., not from a document or other model)
        if message.model == 'mail.channel' and message.res_id:
            channel = self.env['mail.channel'].browse(message.res_id)
            odoo_bot_partner = self.env.ref('odoo_ai.partner_odoo_bot_new')
            partner = message.author_id  # No need to access partner_id, message.author_id is already a res.partner object

            # Log the channel type (general or private)
            if channel.channel_type == 'public':
                _logger.info(f"Message received from the general channel: {channel.name}")
            else:
                _logger.info(f"Message received from a private channel: {channel.name}")

            # Check if the message was sent in a private channel between the user and odooBot (only user and odooBot)
            if len(channel.channel_partner_ids) == 2 and odoo_bot_partner in channel.channel_partner_ids and partner in channel.channel_partner_ids:
                # Ensure the message is sent only by the user and not the bot
                if message.author_id != odoo_bot_partner:
                    # Log the private channel with odooBot and user
                    _logger.info(f"Message received from a private channel between user and odooBot: {channel.name}")

                    # Proceed only if the message is not empty or trivial like "None"
                    user_message = message.body.strip()
                    if not user_message or user_message.lower() in ["none", ""]:
                        _logger.info("Received empty or trivial message, skipping API request.")
                        # Return a default response if the message is invalid
                        self._send_response(channel, odoo_bot_partner, "Please provide a valid question or request.")
                        return message

                    # Proceed with the Gemini API request if the condition is met
                    response_content = self._get_ai_response(user_message)  # Get response from Gemini API

                    # Format the response message (assuming it's in HTML format)
                    formatted_response = self._format_message(response_content)

                    # odooBot responds in the same channel with the correct channel ID
                    try:
                        # Post the message response once (only after processing user input)
                        channel.message_post(
                            body=formatted_response,
                            author_id=odoo_bot_partner.id,
                            message_type='comment',
                            subtype_xmlid='mail.mt_comment',
                            channel_id=channel.id  # Ensure the response is posted in the correct private channel
                        )
                        _logger.info(f"odooBot responded successfully in channel: {channel.name}")
                    except Exception as e:
                        _logger.error(f"Error posting message: {str(e)}")
                else:
                    _logger.info(f"Message sent by odooBot itself. Skipping API request.")
            else:
                # Log if the channel has more members or is public (no API call)
                _logger.info(f"Skipping API call for channel: {channel.name}. Not a private conversation with odooBot and user.")

        return message

    def _get_ai_response(self, user_message):
        """Send the user message to the Gemini API and return the response text."""
        try:
            headers = {
                'Content-Type': 'application/json',
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": user_message
                            }
                        ]
                    }
                ]
            }

            params = {
                'key': self.API_KEY
            }

            _logger.info("Sending request to Gemini API with payload: %s", payload)

            response = requests.post(self.GEMINI_URL, json=payload, headers=headers, params=params, timeout=10)

            _logger.info("Gemini API response: Status: %s, Response: %s", response.status_code, response.json())

            if response.status_code == 200:
                response_data = response.json()
                _logger.info("Gemini API successful response: %s", response_data)

                candidates = response_data.get('candidates', [])
                if not candidates:
                    _logger.warning("No 'candidates' found in Gemini API response.")
                    return _("No response candidates found.")

                first_candidate = candidates[0]
                content = first_candidate.get('content')
                if content:
                    parts = content.get('parts', [])
                    if parts:
                        generated_texts = [part.get('text', '') for part in parts]
                        full_response = ' '.join(generated_texts).strip()
                        _logger.info("Generated AI Response: %s", full_response)
                        return full_response

            else:
                _logger.error("Failed to get a response from Gemini API. Status: %s, Response: %s",
                              response.status_code, response.text)

        except requests.exceptions.RequestException as e:
            _logger.error("Error while connecting to Gemini API: %s", e)

        # Fallback message if API call fails
        return _("I'm having trouble understanding that right now. Please try again later.")

    def _send_response(self, channel, odoo_bot_partner, response_text):
        """Send the response message from odooBot."""
        try:
            # Post the message response
            channel.message_post(
                body=response_text,
                author_id=odoo_bot_partner.id,
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                channel_id=channel.id
            )
            _logger.info(f"odooBot sent a default response: {response_text}")
        except Exception as e:
            _logger.error(f"Error posting default response: {str(e)}")

    def _format_message(self, response_content):
        """Format the response content for better presentation (HTML)."""
        # Basic formatting: Convert newlines to <br/> for line breaks
        response_content = response_content.replace("\n", "<br/>")

        # Bold and styling for headers and section titles
        response_content = response_content.replace("**", "<strong>").replace("**", "</strong>")  # Make text bold
        response_content = response_content.replace("###", "<h3>").replace("###", "</h3>")  # Section headers (H3)

        # Adding horizontal rule (line breaks)
        response_content = response_content.replace("* * *", "<hr />")

        # Adding bullet points styling (List items)
        response_content = response_content.replace("* **", "<ul><li>").replace("**", "</li></ul>")  # Convert bullet points

        return response_content
