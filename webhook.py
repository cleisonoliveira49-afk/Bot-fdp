import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

@app.route("/api/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/set_webhook")
def set_webhook():
    url = os.environ.get("WEBHOOK_URL")
    application.bot.set_webhook(url)
    return f"Webhook set to {url}", 200

async def start(update: Update, context):
    await update.message.reply_text("Olá! Seu bot no Vercel está ativo 🚀")

application.add_handler(CommandHandler("start", start))
