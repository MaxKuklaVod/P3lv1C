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


# Создадим класс состояний
class states(StatesGroup):
  categor = State()
  name = State()


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
Категории:

"""
savedfiles_command_continue = """
Если вы выбрали, напишите ее в новом сообщении так, как она указана здесь.
"""
categories_message = """
Выберете название сохранения, в котором хотите найти свои файлы.
Названия:

"""
categories_message_continue = """
Если вы выбрали, напишите его в новом сообщении так, как оно указано здесь.
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
        if category.count("<") + category.count(">") != 2:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/save <Категория> <Название>"
            )
        elif name.count("<") + name.count(">") != 2:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/save <Категория> <Название>"
            )
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/save <Категория> <Название>"
        )
        return
    global sort
    sort.slovar(category, name, str(message.message_id), str(message.chat.id))

    
#Вывод сообщения по категориям
@dp.message(Command("savedfiles"))
async def main(message, state):
    global sort
    slova = ""
    await message.answer(savedfiles_command + sort.keyses(slova) + savedfiles_command_continue)
    await state.set_state(states.categor)

categor = ''

@dp.message(F.text, states.categor)
async def main(message, state):
    global sort, categor
    slova = ""
    # Обновляем в нашем классе значение categor
    await state.update_data(categor = message.text)
    categor = await state.get_data()
    await message.answer(categories_message + sort.valueses(slova, categor['categor']) + categories_message_continue)
    await state.set_state(states.name)

@dp.message(F.text, states.name)
async def main(message, state):
    global sort, categor
    # Обновляем в нашем классе значение categor
    await state.update_data(name = message.text)
    name = await state.get_data()
    #Вывод сообщения по ID
    chat_id = sort.dict[categor['categor']][name['name']]["chat"]
    message_id = sort.dict[categor['categor']][name['name']]["message"]
    await bot.send_message(chat_id, "Вот ваше сообщение", reply_to_message_id=message_id)
    await state.clear()


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
