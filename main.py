import os
import glob
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def download_video(url):
    ydl_opts = {
    'format': 'worst',
    'outtmpl': '%(id)s.%(ext)s',
    'socket_timeout': 60,
}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Link tashla 🎥\nBot video + mp3 yuboradi 🎵"
    )


@bot.message_handler(func=lambda m: True)
def handle(message):

    try:
        url = message.text

        bot.reply_to(message, "Yuklanyapti... ⏳")

        # eski fayllarni o‘chirish
        for f in glob.glob("*"):
            if f.endswith(".mp4") or f.endswith(".mp3"):
                os.remove(f)

        # video
        download_video(url)

        video_file = glob.glob("*.mp4")[0]

        with open(video_file, "rb") as video:
            bot.send_video(message.chat.id, video)

        # mp3
        download_audio(url)

        audio_file = glob.glob("*.mp3")[0]

        with open(audio_file, "rb") as audio:
            bot.send_audio(message.chat.id, audio)

        # tozalash
        os.remove(video_file)
        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"Xatolik ❌\n{e}")


print("Bot ishladi ✅")

bot.infinity_polling(skip_pending=True)
