import os
import glob
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def clear_files():
    files = glob.glob("*.mp4") + glob.glob("*.webm") + glob.glob("*.m4a") + glob.glob("*.mp3")
    for f in files:
        try:
            os.remove(f)
        except:
            pass


def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'quiet': True,
        'noplaylist': True,'
        'cookiefile': 'cookies.txt',
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
    url = message.text

    bot.reply_to(message, "Yuklanyapti... ⏳")

    clear_files()

    try:
        # VIDEO
        download_video(url)

        video_file = glob.glob("*.mp4")

        if not video_file:
            video_file = glob.glob("*.webm")

        video_file = video_file[0]

        with open(video_file, "rb") as video:
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, video)

        # AUDIO
        download_audio(url)

        audio_file = glob.glob("music.*")[0]

        os.system(f'ffmpeg -i "{audio_file}" music.mp3 -y')

with open("music.mp3", "rb") as audio:
    bot.send_audio(message.chat.id, audio)

        clear_files()

    except Exception as e:
        bot.reply_to(message, f"Xatolik ❌\n{e}")


print("Bot ishga tushdi ✅")

bot.infinity_polling(skip_pending=True)
