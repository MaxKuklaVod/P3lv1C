from aiogram import Bot, Dispatcher
from random import randint
import asyncio
from aiogram.filters.command import Command


Help_Command = """
Список команд:
/help - команда, показывающая список команд
/discription - команда, паказывающая описание бота
/count - команда, считающая кол-во вызовов
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
И Михаил, у которого нет ссылки на телеграмм
Руководитель:
@jezvGG
"""
Count_Command = """
Интересно сколько же я раз до этого вызвал себя?
"""
count = 0


# Создание бота
bot = Bot(token="6523607857:AAFZ3mAetQ5PgZ2otZVhmrMrMcYiZQlseWk")
dp = Dispatcher()


# Команда /start - начальная команда при работе с ботом, которая отпраляет сообщение приветствия
@dp.message(Command("start"))
async def main(message):
    global count
    count += 1
    await message.answer(Start_Command)
    await message.delete()


# Команда /help, которая работает как команда /start
@dp.message(Command("help"))
async def main(message):
    global count
    count += 1
    await message.answer(Help_Command)
    await message.delete()


"""#Перевод из аудио в текст (STT)
@dp.message(content_types=[ContentType.VOICE])
async def audio(message):
    # Download audio file
    file_id = await bot.get_file(message.voice.file_id)
    print(file_id.file_path)
    await bot.download_file(file_id.file_path, 'audio.oga')
    print('Audio saved')

    # Speech-to-Text convertation
    text = STT('audio.oga')"""


# Комадна /discription, которая вызывает описание бота
@dp.message(Command("discription"))
async def main(message):
    global count
    count += 1
    await message.answer(Discription_Command)
    await message.delete()


# Команда для подсчета вызовов
@dp.message(Command("count"))
async def main(message):
    global count
    await message.answer(Count_Command)
    await message.answer(f"Я вызвал себя {count} раз(а)")
    await message.delete()
    count += 1


# Бот будет отвечать на сообщение рандомной буквой алфавита и самим текстом
@dp.message()
async def random_echo(message):
    random_letter = chr(randint(65, 90))
    if message.text.count("0") != 0:
        await message.answer("YES, так как в сообшении есть кое-какая цифра")
    else:
        await message.answer("NO, так как в сообщении кое-чего нет")
    await message.reply(f"Рандомная буква английского алфавита - {random_letter}")


"""#На непонятные сообщения отправляет обратно эхо этого сообщения
@dp.message()
async def echo(message):
    if message.text.count(" ") >= 1:
        await message.answer(message.text.upper())
    else:
        await message.answer("В вашем сообщении менее двух слов, я не буду его повторять ◡‿◡")"""


# Функция, которая запускает программу в боте
asyncio.run(dp.start_polling(bot))
