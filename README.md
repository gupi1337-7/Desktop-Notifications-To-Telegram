# Windows Notification Monitor

This Python script monitors Windows notifications and sends messages about them to a specified Telegram chat. It can detect new letters and chat invites, extract recipient names and invite details, and send customized notifications.

## Features

- Monitors Windows system notifications
- Detects new letters and chat invites
- Extracts recipient names and invite details
- Sends customized notifications to a Telegram chat
- Implements a 5-minute (300-second) delay between notifications
- Handles errors gracefully and continues monitoring

## Requirements

- Windows 10 or 11
- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code.

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a Telegram bot and obtain the bot token:

   - Open Telegram and search for "@BotFather"
   - Start a chat and send "/newbot" to create a new bot
   - Follow the instructions to set up your bot and receive the bot token

4. Get your Telegram Chat ID:

   - Start a chat with your bot
   - Visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates` in your browser
   - Look for the "chat" object in the response and note the "id" field

5. Sign up for an OCR Space account and get your API key:
   - Visit [OCR.Space](https://ocr.space/ocrapi) and sign up for an account
   - Obtain your free API key

## Usage

1. Run the script:

   ```
   python NotWin.py
   ```

2. When prompted, enter your Telegram Bot Token and Chat ID.

3. The script will start monitoring Windows notifications and send customized messages to your Telegram chat.

## Configuration

The script will ask for your Telegram Bot Token and Chat ID when you run it. Make sure to have these ready before starting the script. The OCR API key is currently hardcoded in the script as `OCR_API_KEY`. For security reasons, consider moving this to an environment variable or a separate configuration file.

## Dependencies

This project relies on the following Python libraries:

- pywinauto
- python-telegram-bot
- requests
- mss
- Pillow

These dependencies are listed in the `requirements.txt` file and can be installed using pip.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This script is for educational purposes only. Please ensure you comply with all relevant privacy laws and regulations when monitoring and transmitting notifications. Be aware that using OCR to process screenshots may have privacy implications, especially when dealing with sensitive information.
