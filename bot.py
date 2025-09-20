import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ganti dengan token dari BotFather
BOT_TOKEN = "8218773899:AAFgUbtirvNTIgsyvhZ1BZYCOubUGC5ubW0"

# File untuk simpan user & token
USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! 👋\n\n"
        "Gunakan perintah berikut untuk hubungkan akun FamsssPay:\n"
        "/set_key <token>",
        parse_mode="Markdown"
    )

# /set_key command
async def set_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    user_id = str(update.message.chat_id)

    if len(context.args) == 0:
        await update.message.reply_text("⚠️ Gunakan format: /set_key <token>", parse_mode="Markdown")
        return

    token = context.args[0]
    users[user_id] = {"token": token}
    save_users(users)

    await update.message.reply_text(f"✅ Token berhasil disimpan!\nToken kamu: {token}", parse_mode="Markdown")

# Kirim notifikasi manual (contoh)
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    for uid in users:
        await context.bot.send_message(chat_id=uid, text="🔔 Notifikasi percobaan dari FamsssPay!")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_key", set_key))
    app.add_handler(CommandHandler("notify_all", notify))  # buat testing notif

    print("✅ Bot jalan...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
