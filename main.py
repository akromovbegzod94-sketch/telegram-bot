import os
import telebot
import glob
from yt_dlp import YoutubeDL

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def download_video(url):
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': '%(id)s.%(ext)s',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Link yubor 📥")


@bot.message_handler(func=lambda m: True)
def handle(message):
    url = message.text

    bot.reply_to(message, "Yuklanyapti...")

    try:
        download_video(url)

        video_file = glob.glob("*.mp4")[0]

        video = open(video_file, "rb")

        bot.send_video(message.chat.id, video)

        video.close()

        os.remove(video_file)

    except Exception as e:
        bot.reply_to(message, f"Xatolik ❌\n{e}")


bot.infinity_polling()
