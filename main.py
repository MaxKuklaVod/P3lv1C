from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
import asyncio
from STT import STT_whisper, STT
import json
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


with open("tokens.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)

main_token = tokens["main_token"]

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
Бот умеет писать текст из аудио сообщений🤯. Также позволяет сохранять нужные сообщения по категориям.
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
bot = Bot(token=main_token)
dp = Dispatcher()

# Создание глобальных переменных
sort = []
categories = ["Другое"]
action = ''

# Команда /start - начальная команда при работе с ботом, которая отпраляет сообщение приветствия
@dp.message(Command("start"))
async def main(message):
    await message.answer(start_command)


# Команда /help, которая отправляет список команд
@dp.message(Command("help"))
async def main(message):
    await message.answer(help_command)


# Комадна /discription, которая вызывает описание бота
@dp.message(Command("discription"))
async def main(message):
    await message.answer(discription_command)


# Команда для сохранения сообщения
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
    sort.append({"Категория": categories[0], "Имя": name, "Chat_id": str(message.chat.id), "Message_id": str(message.message_id)})
    await message.reply("Ваше сообщение сохранено")


# Вывод сообщения по категориям
@dp.message(Command("savedfiles"))
async def main(message):
    global categories

    # Инициализируем клавиатуру
    builder = InlineKeyboardBuilder()

    builder.add(*[InlineKeyboardButton(text = item, callback_data = "num_" + item) for item in categories])

    # Указываем клавиатуру в ответе
    builder.adjust(3)
    await message.answer(savedfiles_command, reply_markup=builder.as_markup())


# Вывод сохраненных названий
@dp.callback_query(F.data.startswith("num_"))
async def callback(callback):
    global sort, action

    action = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()

    category = filter(lambda x: x['Категория'] == action, sort)
    builder.add(*[InlineKeyboardButton(text = item["Имя"], callback_data="numm_" + item["Имя"]) for item in category])

    builder.adjust(3)
    await callback.message.answer(categories_message, reply_markup=builder.as_markup())


# Возвращает сохраненное ранее сообщение, по выбранному названию
@dp.callback_query(F.data.startswith("numm_"))
async def callback(callback):
    global sort, action

    name = callback.data.split("_")[1]

    category = filter(lambda x: x['Категория'] == action, sort)
    category = filter(lambda x: x['Имя'] == name, category)

    for item in category:
        await bot.send_message(
        chat_id = item['Chat_id'], text="Вот ваше сообщение", reply_to_message_id = item["Message_id"]
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
