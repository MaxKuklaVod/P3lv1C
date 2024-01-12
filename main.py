from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ContentType
from random import randint
import asyncio
from STT import STT
from aiogram.filters.command import Command
import soundfile as sf
import numpy as np
import speech_recognition as sr
from os import path
from pathlib import Path
from aiogram.fsm.state import StatesGroup, State


Help_Command = """
Отправьте голосовое сообщение и я отправлю вам текст из него🤯
Список команд:
/help - команда, показывающая список команд
/discription - команда, показывающая описание бота
"""
Start_Command = """
Привет!👋 Я бот🤖, который умеет обрабатывать аудио сообщения и присылать их в текстовом формате🤯. \n
/help - команда для получения списка команд
"""
Discription_Command = """
Бот умеет писать текст из аудио сообщений🤯.
Создатели:
@maxkuklavod🙃
@Albert_Nosachenko🤐
@yourocculticT20🧐
Руководитель:
@jezvGG💀
"""

# Создание бота
Token_Bot = "6523607857:AAFZ3mAetQ5PgZ2otZVhmrMrMcYiZQlseWk"
bot = Bot(token=Token_Bot)
dp = Dispatcher()


# Команда /start - начальная команда при работе с ботом, которая отпраляет сообщение приветствия
@dp.message(Command("start"))
async def main(message):
    await bot.send_message(message.from_user.id, Start_Command)
    await message.delete()


# Команда /help, которая работает как команда /start
@dp.message(Command("help"))
async def main(message):
    await bot.send_message(message.from_user.id, Help_Command)
    await message.delete()


# Комадна /discription, которая вызывает описание бота
@dp.message(Command("discription"))
async def main(message):
    await bot.send_message(message.from_user.id, Discription_Command)
    await message.delete()


# Перевод из аудио в текст (STT)
@dp.message(F.content_type == ContentType.VOICE)
async def audio(message):
    # Download audio file
    file_id = await bot.get_file(message.voice.file_id)
    await bot.download_file(file_id.file_path, "audio.ogg")

    # Speech-to-Text convertation
    text = "👋 " + STT("audio.ogg") + " 😘"

    await message.reply(text)


@dp.message(F.content_type == ContentType.TEXT)
async def Hello(message):
    if (
        message.text.count("и че") >= 1
        or message.text.count("И че") >= 1
        or message.text.count("и чё") >= 1
        or message.text.count("И чё") >= 1
    ):
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAJtC2WhNs5jRDj39GBrG9LGAUFt0U8sAAIvKgACWTYQSgyguNjuPct4NAQ",
        )


# Функция, которая запускает программу в боте
asyncio.run(dp.start_polling(bot))
