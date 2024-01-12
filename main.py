from aiogram import Bot, Dispatcher, types
from random import randint
import asyncio
from STT import STT
from aiogram.filters.command import Command
import soundfile as sf
import numpy as np
import speech_recognition as sr
from os import path
from pathlib import Path


Help_Command = """
Список команд:
/help - команда, показывающая список команд
/discription - команда, паказывающая описание бота
"""
Start_Command = """
Привет! Я бот, который умеет обрабатывать аудио сообщения и присылать их в текстовом формате.
Также я умею каждый новый день отправлять расписание. \n
/help - команда для получения списка команд
"""
Discription_Command = """
Бот будет уметь писать текст из аудио сообщений, 
отправлять расписание на день и сохранять данные предметов по папкам.
Создатели:
@maxkuklavod
@Albert_Nosachenko
@yourocculticT20
Руководитель:
@jezvGG
"""

# Создание бота
Token_Bot = "6523607857:AAFZ3mAetQ5PgZ2otZVhmrMrMcYiZQlseWk"
bot = Bot(token=Token_Bot)
dp = Dispatcher()


# Команда /start - начальная команда при работе с ботом, которая отпраляет сообщение приветствия
@dp.message(Command("start"))
async def main(message):
    await message.answer(Start_Command)
    await message.delete()


# Команда /help, которая работает как команда /start
@dp.message(Command("help"))
async def main(message):
    await message.answer(Help_Command)
    await message.delete()


# Комадна /discription, которая вызывает описание бота
@dp.message(Command("discription"))
async def main(message):
    await message.answer(Discription_Command)
    await message.delete()


# Перевод из аудио в текст (STT)
@dp.message()
async def audio(message):
    if message.text == None:
        # Download audio file
        file_id = await bot.get_file(message.voice.file_id)
        await bot.download_file(file_id.file_path, "audio.ogg")

        # Speech-to-Text convertation
        text = STT("audio.ogg")

        await message.reply(text)


# Функция, которая запускает программу в боте
asyncio.run(dp.start_polling(bot))
