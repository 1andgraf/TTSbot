import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultAudio
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters, ContextTypes
import uuid

TELEGRAM_TOKEN = "8235075222:AAHsJ7P_QT0e98o2ZTEQp2WK97d4kcLoFYA"
ELEVEN_API_KEY = "sk_0bfb22057a34aecfa3ee15702bda4cb905044b6938fca49a"

if not TELEGRAM_TOKEN or not ELEVEN_API_KEY:
    raise ValueError("Please set TELEGRAM_TOKEN and ELEVEN_API_KEY environment variables!")

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

VOICES = {
    "Rachel": "EXAVITQu4vr4xnSDxMaL",
    "Bella": "21m00Tcm4TlvDq8ikWAM",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Emma": "QWERTY1234567890ASDFG",
    "Liam": "ZXCVBN0987654321LKJHG",
    "Sophia": "MNBVCXZ1234567890POIU"
}

LANGUAGES = ["🇬🇧 English", "🇪🇸 Spanish", "🇫🇷 French", "🇩🇪 German", "🇮🇹 Italian"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🗣️ Select Voice", callback_data="select_voice"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            InlineKeyboardButton("🌐 Language", callback_data="language_menu")
        ],
        [InlineKeyboardButton("🎤 Generate Audio", callback_data="generate_audio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 *Welcome to TTS Bot\!*\nChoose an option:",
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_to_main":
        if not context.user_data.get("last_message_was_mp3", False):
            await query.message.delete()
        else:
            context.user_data["last_message_was_mp3"] = False

        keyboard = [
            [
                InlineKeyboardButton("🗣️ Select Voice", callback_data="select_voice"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
                InlineKeyboardButton("🌐 Language", callback_data="language_menu")
            ],
            [InlineKeyboardButton("🎤 Generate Audio", callback_data="generate_audio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "🎉 *Welcome to TTS Bot\!*\nChoose an option:",
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )
        return

    await query.message.delete()

    if query.data == "generate_audio":
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Send me the text you want to convert to speech 🎙️", reply_markup=reply_markup)
        context.user_data["awaiting_text"] = True
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "settings":
        volume = context.user_data.get("volume", "Medium")
        speed = context.user_data.get("speed", "Normal")
        stability = context.user_data.get("stability", 0.3)
        keyboard = [
            [InlineKeyboardButton(f"Output Volume: {volume}", callback_data="settings_volume")],
            [InlineKeyboardButton(f"Speed: {speed}", callback_data="settings_speed")],
            [InlineKeyboardButton(f"Stability: {stability}", callback_data="settings_stability")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Settings:", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "settings_volume":
        current = context.user_data.get("volume", "Medium")
        volumes = ["Low", "Medium", "High"]
        idx = (volumes.index(current) + 1) % len(volumes)
        context.user_data["volume"] = volumes[idx]
        speed = context.user_data.get("speed", "Normal")
        stability = context.user_data.get("stability", 0.3)
        keyboard = [
            [InlineKeyboardButton(f"Output Volume: {volumes[idx]}", callback_data="settings_volume")],
            [InlineKeyboardButton(f"Speed: {speed}", callback_data="settings_speed")],
            [InlineKeyboardButton(f"Stability: {stability}", callback_data="settings_stability")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Settings:", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "settings_speed":
        current = context.user_data.get("speed", "Normal")
        speeds = ["Slow", "Normal", "Fast"]
        idx = (speeds.index(current) + 1) % len(speeds)
        context.user_data["speed"] = speeds[idx]
        volume = context.user_data.get("volume", "Medium")
        stability = context.user_data.get("stability", 0.3)
        keyboard = [
            [InlineKeyboardButton(f"Output Volume: {volume}", callback_data="settings_volume")],
            [InlineKeyboardButton(f"Speed: {speeds[idx]}", callback_data="settings_speed")],
            [InlineKeyboardButton(f"Stability: {stability}", callback_data="settings_stability")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Settings:", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "settings_stability":
        current = context.user_data.get("stability", 0.3)
        stabilities = [0.0, 0.3, 0.6, 1.0]
        try:
            idx = (stabilities.index(float(current)) + 1) % len(stabilities)
        except ValueError:
            idx = 1
        context.user_data["stability"] = stabilities[idx]
        volume = context.user_data.get("volume", "Medium")
        speed = context.user_data.get("speed", "Normal")
        keyboard = [
            [InlineKeyboardButton(f"Output Volume: {volume}", callback_data="settings_volume")],
            [InlineKeyboardButton(f"Speed: {speed}", callback_data="settings_speed")],
            [InlineKeyboardButton(f"Stability: {stabilities[idx]}", callback_data="settings_stability")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Settings:", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "settings_language":
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "select_voice":
        current_voice_id = context.user_data.get("voice_id", VOICE_ID)
        keyboard = []
        for name, voice_id in VOICES.items():
            label = f"{name} {'✅' if voice_id == current_voice_id else ''}"
            keyboard.append([InlineKeyboardButton(label, callback_data=f"voice_{voice_id}")])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select a voice:", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data == "language_menu":
        current_language = context.user_data.get("language", "English")
        keyboard = []
        for lang in LANGUAGES:
            label = f"{lang} {'✅' if lang == current_language else ''}"
            keyboard.append([InlineKeyboardButton(label, callback_data=f"set_language_{lang}")])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select a language:", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data.startswith("set_language_"):
        selected_language = query.data[len("set_language_"):]
        context.user_data["language"] = selected_language
        keyboard = [
            [
                InlineKeyboardButton("🌐 Language", callback_data="language_menu"),
                InlineKeyboardButton("🗣️ Select Voice", callback_data="select_voice"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings")
            ],
            [InlineKeyboardButton("🎤 Generate Audio", callback_data="generate_audio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Language set to {selected_language}!", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

    elif query.data.startswith("voice_"):
        selected_voice_id = query.data[len("voice_"):]
        context.user_data["voice_id"] = selected_voice_id
        keyboard = [
            [
                InlineKeyboardButton("🎤 Generate Audio", callback_data="generate_audio"),
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Voice selected! You can now generate audio with this voice.", reply_markup=reply_markup)
        context.user_data["last_message_was_mp3"] = False

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_text"):
        await update.message.reply_text("Please use the buttons from the start menu.")
        return

    user_text = update.message.text.strip()
    if not user_text:
        await update.message.reply_text("⚠️ Please send some text!")
        return

    voice_id = context.user_data.get("voice_id", VOICE_ID)
    stability = context.user_data.get("stability", 0.3)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVEN_API_KEY}
    data = {
        "text": user_text,
        "voice_settings": {"stability": stability, "similarity_boost": 0.7}
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.HTTPError:
        await update.message.reply_text(f"⚠️ ElevenLabs error: {response.status_code} {response.text}")
        return
    except requests.RequestException as e:
        await update.message.reply_text(f"⚠️ Network error: {e}")
        return

    audio_path = "output.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)

    try:
        with open(audio_path, "rb") as f:
            await update.message.reply_voice(voice=f)
        with open(audio_path, "rb") as f:
            keyboard = [
                [InlineKeyboardButton("🎤 Generate Audio", callback_data="generate_audio")],
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            sent_message = await update.message.reply_document(document=f, reply_markup=reply_markup)
            context.user_data["last_message_was_mp3"] = True
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    context.user_data["awaiting_text"] = False

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return

    voice_id = VOICE_ID
    stability = 0.3
    if context.user_data:
        voice_id = context.user_data.get("voice_id", VOICE_ID)
        stability = context.user_data.get("stability", 0.3)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVEN_API_KEY}
    data = {
        "text": query,
        "voice_settings": {"stability": stability, "similarity_boost": 0.7}
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        return

    audio_bytes = response.content
    audio_file_id = str(uuid.uuid4())
    audio_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/tmp/{audio_file_id}.mp3"

    results = [
        InlineQueryResultAudio(
            id=audio_file_id,
            audio_url="https://file-examples.com/storage/fe0b6a0f0e6af0e6f5f9aaf/2017/11/file_example_MP3_700KB.mp3",
            title="TTS Audio",
            caption=query,
            performer="TTS Bot"
        )
    ]

    await update.inline_query.answer(results, cache_time=0, is_personal=True)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))
    app.add_handler(InlineQueryHandler(inline_query_handler))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()