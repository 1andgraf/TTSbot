# VoiceBot Telegram Bot

Welcome to **VoiceBot**, a powerful Telegram bot that brings advanced Text-to-Speech (TTS) capabilities right to your fingertips. Whether you want to convert text messages into natural-sounding audio or use inline queries to generate speech on the fly, VoiceBot makes it easy and fun!

---

## Project Overview

VoiceBot is a Telegram bot designed to convert text into high-quality speech using the ElevenLabs API. It supports multiple voices and languages, allowing users to customize their audio output. The bot features an intuitive interface with inline queries, voice and language selection, and adjustable settings such as volume, speed, and stability.

---

## Features

- **High-Quality Text-to-Speech:** Converts your text messages into natural-sounding audio using ElevenLabs' advanced voice synthesis.
- **Multiple Voices:** Choose from a variety of voices including Rachel, Bella, Antoni, Emma, Liam, and Sophia.
- **Language Support:** Supports multiple languages such as English, Spanish, French, German, and Italian.
- **Customizable Settings:** Adjust output volume, speed, and voice stability to tailor the audio to your preference.
- **Background Music Support:** Enhance your audio with background music options.
- **Inline Queries:** Generate TTS audio directly from any chat via inline queries without leaving the conversation.
- **User-Friendly Interface:** Easy navigation through voice selection, language settings, and audio generation via inline buttons.

---

## Setup & Installation

To set up VoiceBot on your own server or local machine, follow these steps:

1. **Clone the Repository:**

```bash
git clone https://github.com/yourusername/voicebot.git
cd voicebot
```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

3. **Obtain API Keys:**

- **Telegram Bot Token:** Create a bot via [BotFather](https://t.me/BotFather) on Telegram and get your token.
- **ElevenLabs API Key:** Sign up at [ElevenLabs](https://elevenlabs.io/) and generate an API key.

4. **Configure Environment Variables:**

```bash
export TELEGRAM_TOKEN="your_telegram_token_here"
export ELEVEN_API_KEY="your_elevenlabs_api_key_here"
```

5. **Run the Bot:**

```bash
python app.py
```

---

## Usage

Start your bot by sending the `/start` command in Telegram. The bot will present you with a menu:

- **🗣️ Select Voice:** Choose your preferred voice for TTS.
- **⚙️ Settings:** Adjust volume, speed, and stability for audio output.
- **🌐 Language:** Select the language for your TTS.
- **🎤 Generate Audio:** Send text to convert it into speech.

Simply select **Generate Audio**, type your text, and receive a high-quality audio message in response.

---

## Inline Queries

VoiceBot supports inline queries, enabling you to generate speech directly from any chat without opening the bot:

1. In any Telegram chat, type `@YourBotUsername your text here`.
2. The bot will return audio results you can send instantly.
3. Customize voice and settings via the bot menu for personalized inline query results.

---

## Settings

VoiceBot allows you to customize your TTS experience:

- **Output Volume:** Choose from Low, Medium, or High.
- **Speed:** Adjust speech speed between Slow, Normal, and Fast.
- **Stability:** Control voice stability for more natural or consistent speech.
- **Voice Selection:** Switch between multiple available voices.
- **Language Selection:** Pick your preferred language for TTS.

Settings are accessible via the main menu and are saved per user for convenience.

---

## Contributing

Contributions are welcome! If you'd like to improve VoiceBot, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear messages.
4. Submit a pull request describing your improvements.

Please ensure your code adheres to existing style and includes appropriate tests.

---

## License

VoiceBot is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as you wish.

---

Thank you for using VoiceBot! If you have any questions or feedback, please open an issue on GitHub or contact the maintainer.

