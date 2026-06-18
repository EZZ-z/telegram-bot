from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8635975989:AAEOriz1Kn6Ql6DjEkssjhfWHaSJVwrapss"

async def handle_any(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.audio:
        fid = msg.audio.file_id
        print(f"\n✅ FILE_ID: {fid}\n")
        await msg.reply_text(f"file_id:\n{fid}")
    elif msg.voice:
        fid = msg.voice.file_id
        print(f"\n✅ FILE_ID: {fid}\n")
        await msg.reply_text(f"file_id:\n{fid}")
    elif msg.document:
        fid = msg.document.file_id
        print(f"\n✅ FILE_ID: {fid}\n")
        await msg.reply_text(f"file_id:\n{fid}")
    else:
        await msg.reply_text("ابعتلي ملف صوتي")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_any))
    print("شغال - ابعتلي ملف صوتي ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
