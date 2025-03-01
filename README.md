# Odoo-Bot

## Overview
Odoo-Bot is an AI-powered chatbot integrated into Odoo, utilizing the Gemini API for generating bot responses. The bot operates as a system user within Odoo and facilitates chat interactions through private channels, leveraging the Discuss module interface.

## Features
- **AI-Powered Chatbot**: Utilizes Gemini API to generate responses.
- **Odoo Integration**: Seamlessly embedded as a system user within Odoo.
- **Private Channel Communication**: Users can interact with the bot through private channels.
- **Discuss Interface**: Uses Odoo's Discuss module for a familiar chat experience.

## Installation
### Prerequisites
- Odoo (version compatible with Discuss module)
- Python 3.x
- Odoo Addons directory access
- API Key for Gemini

## Usage
- Open the **Discuss** module in Odoo.
- Start a private conversation with the bot (System User).
- The bot will respond using the Gemini API.

## Configuration
Modify `config.py` to update bot behavior and API settings:
```python
GEMINI_API_KEY = "your_api_key_here"
BOT_NAME = "OdooBot"
```

## Troubleshooting
- **Bot not responding?** Ensure the API key is correctly set.
- **Odoo restart issues?** Check logs for module loading errors.
- **Incorrect responses?** Verify Gemini API connectivity.

## License
This project is licensed under the MIT License.

## Contributors
- Sangram Shinde

