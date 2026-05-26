import os
import glob
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def clear_files():
    for f in glob.glob("*"):
        if f.endswith((".mp4", ".webm", ".m4a", ".mp3", ".mkv")):
            try:
                os.remove(f)
            except:
                pass


def download_video(url):
    ydl_opts = {
        'format': 'worst',
        'outtmpl': '%(id)s.%(ext)s',
        'socket_timeout': 60,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'noplaylist': True,
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

    try:

        # VIDEO
        download_video(url)

        video_files = (
            glob.glob("*.mp4") +
            glob.glob("*.webm") +
            glob.glob("*.mkv")
        )

        video_file = video_files[0]

        with open(video_file, "rb") as video:
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, video)

        # AUDIO
        download_audio(url)

        audio_file = glob.glob("music.*")[0]

        os.system(f'ffmpeg -i "{audio_file}" music.mp3 -y')

        with open("music.mp3", "rb") as audio:
            bot.send_audio(
                message.chat.id,
                audio,
                title="Audio yuklandi 🎵"
            )

        clear_files()

    except Exception as e:
        bot.reply_to(message, f"Xatolik ❌\n{e}")


bot.infinity_polling()
