import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DB_FILE = "database.json"

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /buy to get key")

async def addkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Use /addkey KEY")
        return

    db = load_db()
    db["keys"].append(context.args[0])
    save_db(db)

    await update.message.reply_text("✅ Key Added")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()

    if len(db["keys"]) == 0:
        await update.message.reply_text("❌ No keys available")
        return

    key = db["keys"].pop(0)
    save_db(db)

    await update.message.reply_text(f"✅ Your Key:\n{key}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addkey", addkey))
app.add_handler(CommandHandler("buy", buy))

print("Bot running...")
app.run_polling()
