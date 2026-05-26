import os
import glob
import telebot
from yt_dlp import YoutubeDL
from ShazamAPI import Shazam

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def clear_files():
    for f in glob.glob("*"):
        if f.endswith((".mp4", ".webm", ".m4a", ".mp3")):
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


def recognize_music(file):
    mp3_file_content_to_recognize = open(file, 'rb').read()

    shazam = Shazam(mp3_file_content_to_recognize)

    try:
        recognize_generator = shazam.recognizeSong()
        result = next(recognize_generator)

        track = result[1]["track"]

        title = track["title"]
        artist = track["subtitle"]

        return f"{artist} - {title}"

    except:
        return "Topilmadi"


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

        video_file = glob.glob("*.mp4")[0]

        with open(video_file, "rb") as video:
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, video)

        # AUDIO
        download_audio(url)

        audio_file = glob.glob("music.*")[0]

        os.system(f'ffmpeg -i "{audio_file}" music.mp3 -y')

        music_name = recognize_music("music.mp3")

        with open("music.mp3", "rb") as audio:
            bot.send_audio(
                message.chat.id,
                audio,
                title=music_name
            )

        bot.send_message(
            message.chat.id,
            f"🎵 Music: {music_name}"
        )

        clear_files()

    except Exception as e:
        bot.reply_to(message, f"Xatolik ❌\n{e}")


bot.infinity_polling()
