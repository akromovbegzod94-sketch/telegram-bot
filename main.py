import os
import glob
import asyncio
import yt_dlp

from aiogram import Bot, Dispatcher
from aiogram.types import (
Message,
ReplyKeyboardMarkup,
KeyboardButton,
FSInputFile,
InlineKeyboardMarkup,
InlineKeyboardButton
)
from aiogram.filters import CommandStart
from groq import Groq

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = Groq(api_key=OPENAI_API_KEY)

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

@dp.message(CommandStart())
async def start(message: Message):
await message.answer(
"Добро пожаловать 🤖",
reply_markup=menu
)

@dp.message()
async def all_messages(message: Message):

```
text = message.text or ""

if text == "🎵 Музыка":
    await message.answer(
        "Отправь название песни 🎵",
        reply_markup=menu
    )
    return

if text == "🎬 Скачать видео":
    await message.answer(
        "Отправь ссылку TikTok / YouTube / Instagram 🎬",
        reply_markup=menu
    )
    return

if text == "🤖 AI":
    await message.answer(
        "Напиши вопрос 🤖",
        reply_markup=menu
    )
    return

if text == "🎤 Найти песню":
    await message.answer(
        "Отправь голосовое сообщение 🎤",
        reply_markup=menu
    )
    return

if "http" in text:

    await message.answer("Скачиваю видео... ⏳")

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s",
        "noplaylist": True
    }

    try:
        for f in glob.glob("video.*"):
            os.remove(f)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])

        video_files = glob.glob("video.*")

        if not video_files:
            await message.answer("Видео не найдено ❌")
            return

        video_file = FSInputFile(video_files[0])

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎵 Найти музыку",
                        callback_data="find_music"
                    )
                ]
            ]
        )

        await message.answer_video(
            video=video_file,
            reply_markup=keyboard
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")

    return

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
    await message.answer(f"AI ошибка: {e}")
```

async def main():
print("Бот запущен 🚀")
await dp.start_polling(bot)

if **name** == "**main**":
asyncio.run(main())
