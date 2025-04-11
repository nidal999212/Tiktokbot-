
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import re
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def download_tiktok_video(url):
    try:
        api_url = f"https://tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        if response.get("data"):
            return response["data"]["play"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url_pattern = r"(https?://[^\s]+)"
    message = update.message.text
    match = re.search(url_pattern, message)
    
    if match:
        url = match.group(0)
        await update.message.reply_text("جارٍ تحميل الفيديو...")
        video_url = download_tiktok_video(url)
        
        if video_url:
            await update.message.reply_video(video=video_url, caption="هاهو الفيديو من TikTok")
        else:
            await update.message.reply_text("تعذر تحميل الفيديو. تأكد أن الرابط صحيح.")
    else:
        await update.message.reply_text("أرسل رابط فيديو تيك توك فقط.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط فيديو من تيك توك وسأقوم بتحميله لك.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
