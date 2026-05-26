import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

def download_video(url):
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': 'video.mp4',
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

        video = open("video.mp4", "rb")
        bot.send_video(message.chat.id, video)

    except:
        bot.reply_to(message, "Xatolik ❌")

bot.polling()
