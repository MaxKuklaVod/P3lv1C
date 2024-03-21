from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
import asyncio
import random
from STT import STT, Punct
from messege_bd import data_base as db
import json
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from threading import Timer

with open("tokens.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)

main_token = tokens["main_token"]

with open("textconst.json", encoding="utf-8") as complex_data:
    data = complex_data.read()
    const = json.loads(data)

help_command = const["help"]
start_command = const["start"]
discription_command = const["discription"]
savedfiles_command = const["savedfiles"]
categories_message = const["categories"]
everytenmin = const["tenmin"]


# Создание бота
bot = Bot(token=main_token)
dp = Dispatcher()

# Создание глобальных переменных
sort = []
categories = []
members = {}
action = ""
Admin_ID = 0
bd = db("P3lv1c_bone.db")
bd.start()
bd.create(
    "saves",
    {
        "mes_id": "text",
        "chat_id": "text",
        "id_category": "integer",
        "name": "text",
    },
)
for i in range(1, 8):
    categories.append(bd.get("categories", {"id": i})[1])

bd.stop()


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
    global categories, id_category
    category = category.lower()
    # мега костыль
    if category == "информационные":
        category = "информационные системы и технологии"
        name = name[21:]
    elif category == "компьютерное":
        category = "компьютерное зрение"
        name = name[7:]
    elif category == "русский":
        category = "русский язык"
        name = name[5:]
    elif category == "шаблоны":
        category = "шаблоны проектирования"
        name = name[15:]

    bd.start()
    if category not in categories:
        id_category = bd.get("categories", {"name": "другое"})[0]
        bd.insert(
            "saves",
            {
                "mes_id": str(message.message_id),
                "chat_id": str(message.chat.id),
                "id_category": id_category,
                "name": name,
            },
        )
        await message.reply(
            f"Так как еще нет категории <{category}> Ваше сообщение сохранено, в категорию: <Другое>"
        )
    else:
        id_category = bd.get("categories", {"name": category})[0]
        bd.insert(
            "saves",
            {
                "mes_id": str(message.message_id),
                "chat_id": str(message.chat.id),
                "id_category": id_category,
                "name": name,
            },
        )
        await message.reply("Ваше сообщение сохранено")
    bd.stop()


# Вывод сообщения по категориям
@dp.message(Command("savedfiles"))
async def main(message):
    global categories, chat_id
    chat_id = message.chat.id
    # Инициализируем клавиатуру
    builder = InlineKeyboardBuilder()
    builder.add(
        *[
            InlineKeyboardButton(
                text=item.capitalize(), callback_data="num_" + f"{num}"
            )
            for num, item in enumerate(categories)
        ]
    )

    # Указываем клавиатуру в ответе
    builder.adjust(1)
    await message.answer(savedfiles_command, reply_markup=builder.as_markup())
    await message.delete()


# Вывод сохраненных названий
@dp.callback_query(F.data.startswith("num_"))
async def callback(callback):
    global action, chat_id
    bd.start()
    action = int(callback.data.split("_")[1]) + 1
    builder = InlineKeyboardBuilder()

    names = bd.get_raw("saves", {"id_category": action, "chat_id": chat_id})
    bd.stop()
    builder.add(
        *[
            InlineKeyboardButton(text=item[3], callback_data="numm_" + item[0])
            for item in names
        ]
    )

    builder.adjust(3)
    await callback.message.answer(categories_message, reply_markup=builder.as_markup())
    await callback.message.delete()


# Возвращает сохраненное ранее сообщение, по выбранному названию
@dp.callback_query(F.data.startswith("numm_"))
async def callback(callback):
    global chat_id
    message = callback.data.split("_")[1]
    await bot.send_message(
        chat_id=chat_id,
        text="Вот ваше сообщение",
        reply_to_message_id=message,
    )
    await callback.message.delete()


def punctuation():
    _ = Punct(everytenmin)
    print(_)
    Timer(600, punctuation).start()


punctuation()


# Перевод из аудио в текст (STT)
@dp.message(F.content_type == ContentType.VOICE)
async def audio(message):
    edittext = ""
    # Download audio file
    file_id = await bot.get_file(message.voice.file_id)
    await bot.download_file(file_id.file_path, "audio.ogg")

    # Speech-to-Text convertation
    edittext = STT("audio.ogg")

    msg = await message.reply(edittext)

    punctual = Punct(edittext)
    await bot.edit_message_text(
        chat_id=str(message.chat.id), message_id=str(msg.message_id), text=punctual
    )


# Очередь для математики
@dp.message(Command("stmath"))
async def Math(message):
    global members
    members.clear()

    await message.answer(
        "Кто хочет участвовать в очереди, напишите любое сообщение. Когда закончите, напишите команду /edmath"
    )


# Вывод очереди
@dp.message(Command("edmath"))
async def Math(message):
    global members
    conclusion = ""

    for i in range(len(members)):
        random_member = random.choice(members.values())
        conclusion += random_member + "\n"
        members = {key: val for key, val in members.items() if val != random_member}

    await message.answer("Вот ваша очередь: \n" + conclusion)


# Создание списка людей в группе
@dp.message(F.content_type == ContentType.TEXT)
async def Math(message):
    global members

    firstname = message.from_user.first_name
    username = message.from_user.username
    userid = message.from_user.id
    member = "@" + username + " - " + firstname

    if userid not in members.keys():
        members[userid] = member

    if (
        "и" in message.text.lower().split()
        and "че" in message.text.lower().split()
        or "чё" in message.text.lower().split()
    ):
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAJtC2WhNs5jRDj39GBrG9LGAUFt0U8sAAIvKgACWTYQSgyguNjuPct4NAQ",
        )

    if "лебед" in message.text.lower() or "не растраивайся" in message.text.lower():
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAEEMrNl-9zOgfrh6GJz2n9EEy9c90jVOwACl1EAAvj6aEu3ZxRrYYnWIDQE",
        )
    if (
        "пойдешь?" in message.text.lower()
        or "пойдёшь?" in message.text.lower()
        or "го?" in message.text.lower()
    ):
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAEEMsVl-99H7tSaTw7pGicmX8U2MVAitQACZ0cAAsRFaEvviMV6epKAgzQE",
        )
    if "круто" in message.text.lower():
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAEEMsdl-9_GcjSK1rwFNntWiMRAepgcXwACgCUAAlWNCEpk32eI4XKYATQE",
        )


# Функция, которая запускает программу в боте
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
