from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ContentType
import asyncio
from STT import STT
from sorted import Sorting
from TokenBot import token_bot
from aiogram.filters.command import Command
import soundfile as sf
import numpy as np
import speech_recognition as sr
from os import path
from pathlib import Path
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


help_command = """
Отправьте голосовое сообщение и я отправлю вам текст из него🤯
Список команд:
/help - команда, показывающая список команд
/discription - команда, показывающая описание бота
/save <Категория> <Название> - команда для сохранения картинок/фотографий по категориям
/savedfiles - команда, с помощью которой вы можете обратиться к сохраненным сообщениям
"""
start_command = """
Привет!👋 Я бот🤖, который умеет обрабатывать аудио сообщения и присылать их в текстовом формате🤯. \n
/help - команда для получения списка команд
"""
discription_command = """
Бот умеет писать текст из аудио сообщений🤯.
Создатели:
@maxkuklavod🙃
@Albert_Nosachenko🤐
@yourocculticT20🧐
Руководитель:
@jezvGG💀
"""
savedfiles_command = """
Выберете категорию сохранения, в которой хотите найти свои файлы.
"""
categories_message = """
Выберете название сохранения, в котором хотите найти свои файлы.
"""

# Создание бота
bot = Bot(token=token_bot)
dp = Dispatcher()


# Команда /start - начальная команда при работе с ботом, которая отпраляет сообщение приветствия
@dp.message(Command("start"))
async def main(message):
    await message.answer(start_command)


# Команда /help, которая работает как команда /start
@dp.message(Command("help"))
async def main(message):
    await message.answer(help_command)


# Комадна /discription, которая вызывает описание бота
@dp.message(Command("discription"))
async def main(message):
    await message.answer(discription_command)


# Команда сортировки по категориям
sort = Sorting()
slova = []
name = []
categories = []


@dp.message(Command("save"))
async def main(message, command):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        category, name = command.args.split(" ", maxsplit=1)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/save <Категория> <Название>"
        )
        return
    global sort, categories
    sort.slovar("Другое", name, str(message.message_id), str(message.chat.id))
    await message.reply("Ваше сообщение сохранено")


# Вывод сообщения по категориям, работает отлично
@dp.message(Command("savedfiles"))
async def main(message):
    global sort, slova

    # Инициализируем клавиатуру
    builder = InlineKeyboardBuilder()

    sort.keyses(slova)
    slova = list(set(slova))

    for i in range(len(slova)):
        builder.add(InlineKeyboardButton(text=slova[i], callback_data="num_" + str(i)))

    # Указываем клавиатуру в ответе
    builder.adjust(3)
    await message.answer(savedfiles_command, reply_markup=builder.as_markup())


# Работает отлично, показывает наименование сохраненок
@dp.callback_query(F.data.startswith("num_"))
async def callback(callback):
    global sort, slova, name

    action = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()

    slova = list(set(slova))

    for i in range(len(slova)):
        if action == str(i):
            sort.valueses(name, slova[i])
            name = list(set(name))
            for j in range(len(name)):
                builder.add(
                    InlineKeyboardButton(
                        text=name[j], callback_data="numm_" + str(j) + str(j)
                    )
                )
    builder.adjust(3)
    await callback.message.answer(categories_message, reply_markup=builder.as_markup())


# Работает отлично, возвращает сохраненное ранее сообщение
@dp.callback_query(F.data.startswith("numm_"))
async def callback(callback):
    global sort, slova, name

    slova = list(set(slova))
    name = list(set(name))

    action = callback.data.split("_")[1]

    for i in range(len(slova)):
        sort.valueses(name, slova[i])
        for j in range(len(name)):
            if action == str(i) * 2:
                chatid = sort.dict[slova[i]][name[j]]["chat"]
                message_id = sort.dict[slova[i]][name[j]]["message"]
            else:
                continue
    await bot.send_message(
        chat_id=chatid, text="Вот ваше сообщение", reply_to_message_id=message_id
    )


# Перевод из аудио в текст (STT)
@dp.message(F.content_type == ContentType.VOICE)
async def audio(message):
    # Download audio file
    file_id = await bot.get_file(message.voice.file_id)
    await bot.download_file(file_id.file_path, "audio.ogg")

    # Speech-to-Text convertation
    text = STT("audio.ogg")

    await message.reply(text)


# Пасхалка с Игорем
@dp.message(F.content_type == ContentType.TEXT)
async def Hello(message):
    if "и чё" in message.text.lower() or "и че" in message.text.lower():
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAJtC2WhNs5jRDj39GBrG9LGAUFt0U8sAAIvKgACWTYQSgyguNjuPct4NAQ",
        )


# Функция, которая запускает программу в боте
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
