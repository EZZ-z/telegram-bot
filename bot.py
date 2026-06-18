import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

DATA = {
    "📖 شرح التجويد": {
        "درس ١ - باب الصفات": {
            "type": "audio",
            "file_id": "CQACAgQAAxkBAAPaajPv7V8t8ooQy91ct6elR_r5io8AAmceAAL-96BRmDqOpsygnfw8BA",
            "caption": "باب الصفات"
        },
    },
    "🌿 قراءة سورة البقرة": {
    },
}

BOT_TOKEN = "8635975989:AAEOriz1Kn6Ql6DjEkssjhfWHaSJVwrapss"
ADMIN_ID = 1409085038

def main_menu_keyboard():
    buttons = [[KeyboardButton(section)] for section in DATA.keys()]
    buttons.append([KeyboardButton("🏠 الرئيسية")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def lessons_keyboard(section_name):
    lessons = list(DATA[section_name].keys())
    buttons = [[KeyboardButton(lesson)] for lesson in lessons]
    buttons.append([KeyboardButton("🔙 رجوع")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def find_lesson(lesson_name):
    for section, lessons in DATA.items():
        if lesson_name in lessons:
            return section, lessons[lesson_name]
    return None, None

def find_section(text):
    for section in DATA.keys():
        if text == section:
            return section
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "السلام عليكم ورحمة الله 👋\n\nاختر القسم اللي تريده:",
        reply_markup=main_menu_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    current_section = context.user_data.get("section")

    if text in ["🏠 الرئيسية", "🔙 رجوع", "/start"]:
        context.user_data.clear()
        await update.message.reply_text(
            "اختر القسم:",
            reply_markup=main_menu_keyboard()
        )
        return

    section = find_section(text)
    if section:
        context.user_data["section"] = section
        lessons = DATA[section]
        if not lessons:
            await update.message.reply_text(
                "⚠️ مفيش دروس في القسم ده لسه",
                reply_markup=main_menu_keyboard()
            )
            return
        await update.message.reply_text(
            f"اخترت: {section}\n\nاختر الدرس:",
            reply_markup=lessons_keyboard(section)
        )
        return

    if current_section:
        _, lesson_data = find_lesson(text)
        if lesson_data:
            file_id = lesson_data["file_id"]
            caption = lesson_data.get("caption", text)
            if lesson_data["type"] == "audio":
                await update.message.reply_audio(audio=file_id, caption=caption)
            elif lesson_data["type"] == "video":
                await update.message.reply_video(video=file_id, caption=caption)
            elif lesson_data["type"] == "document":
                await update.message.reply_document(document=file_id, caption=caption)
            elif lesson_data["type"] == "photo":
                await update.message.reply_photo(photo=file_id, caption=caption)
            return

    await update.message.reply_text(
        "اختر من القائمة 👇",
        reply_markup=main_menu_keyboard() if not current_section else lessons_keyboard(current_section)
    )

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.audio:
        await update.message.reply_text(f'file_id = "{update.message.audio.file_id}"')
    elif update.message.document:
        await update.message.reply_text(f'file_id = "{update.message.document.file_id}"')
    elif update.message.photo:
        await update.message.reply_text(f'file_id = "{update.message.photo[-1].file_id}"')
    elif update.message.video:
        await update.message.reply_text(f'file_id = "{update.message.video.file_id}"')

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.AUDIO | filters.Document.ALL | filters.PHOTO | filters.VIDEO,
        get_file_id
    ))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت شغال ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
