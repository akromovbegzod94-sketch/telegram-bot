import os
import glob
import asyncio
import yt_dlp

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import CommandStart
from groq import Groq

# ====== TOKENS ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ====== BOT ======
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = Groq(api_key=OPENAI_API_KEY)

# ====== MENU ======
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎵 Музыка"),
            KeyboardButton(text="🎬 Скачать видео")
        ],
        [
            KeyboardButton(text="🤖 AI"),
            KeyboardButton(text="🎤 Найти песню")
        ]
    ],
    resize_keyboard=True
)

# ====== START ======
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Добро пожаловать 🤖",
        reply_markup=menu
    )

# ====== MAIN ======
@dp.message()
async def all_messages(message: Message):

    text = message.text

    # ====== MUSIC ======
    if text == "🎵 Музыка":
        await message.answer(
            "Отправь название песни 🎵"
        )
        return

    # ====== VIDEO ======
    if text == "🎬 Скачать видео":
        await message.answer(
            "Отправь ссылку TikTok / YouTube / Instagram 🎬"
        )
        return

    # ====== FIND SONG ======
    if text == "🎤 Найти песню":
        await message.answer(
            "Отправь голосовое сообщение 🎤"
        )
        return

    # ====== DOWNLOAD VIDEO ======
    if "http" in text:

        await message.answer("Скачиваю видео... ⏳")

        ydl_opts = {
            "format": "best",
            "outtmpl": "video.%(ext)s",
            "noplaylist": True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])

            video_files = glob.glob("video.*")

            if not video_files:
                await message.answer("Видео не найдено ❌")
                return

            video_file = video_files[0]
            video_file = FSInputFile(video_file)
            
                await message.answer_video(video=video_file)

        except Exception as e:
            await message.answer(
                f"Ошибка: {e}"
            )

        return

    # ====== AI ======
    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        reply = response.choices[0].message.content

        await message.answer(reply)

    except Exception as e:
        await message.answer(
            f"AI ошибка: {e}"
        )

# ====== START BOT ======
async def main():
    print("Бот запущен 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
