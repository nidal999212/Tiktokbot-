import os
from telegram import Update, InputFile
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp
import uuid
import subprocess
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def handle_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("جاري المعالجة...")

    unique_id = str(uuid.uuid4())
    video_path = f"{unique_id}.mp4"
    audio_path = f"{unique_id}.mp3"
    thumbnail_path = f"{unique_id}.jpg"

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': video_path,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "TikTok Audio")
            duration = int(info.get("duration", 0))
            thumbnail = info.get("thumbnail", "")

        subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-q:a", "3", audio_path], check=True)

        if thumbnail:
            with open(thumbnail_path, "wb") as f:
                f.write(requests.get(thumbnail).content)
            thumb = InputFile(thumbnail_path)
        else:
            thumb = None

        await update.message.reply_audio(
            audio=InputFile(audio_path),
            title=title,
            duration=duration,
            thumbnail=thumb
        )
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"حدث خطأ: {e}")

    finally:
        for f in [video_path, audio_path, thumbnail_path]:
            if os.path.exists(f):
                os.remove(f)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tiktok))
    app.run_polling()

if __name__ == "__main__":
    main()
