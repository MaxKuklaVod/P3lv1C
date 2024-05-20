from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
import asyncio
import random
from DopClasses.STT import STT, STT_whisper
from DopClasses.messege_bd import db_manager as db
import json
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pathlib import Path
import datetime
import juliandate

with open(Path(__file__).parent / "Json" / "tokens.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)

main_token = tokens["test_token"]

with open(
    Path(__file__).parent / "Json" / "textconst.json", encoding="utf-8"
) as complex_data:
    data = complex_data.read()
    const = json.loads(data)

help_command = const["help"]
start_command = const["start"]
discription_command = const["discription"]
savedfiles_command = const["savedfiles"]
categories_message = const["categories"]


# Создание бота
bot = Bot(token=main_token)
dp = Dispatcher()

# Создание глобальных переменных
sort = []
categories = []
members = {}
chat = ""
user_id = 0
save_message = ""
action = ""
flag = False
discipline_id = 0
Admin_ID = 0
bd = db("P3lv1c_bone.db")


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
async def main(message):

    global user_id, chat_id, mes_id

    user_id = message.from_user.id
    chat_id = message.chat.id
    mes_id = message.message_id

    bd.start()

    day_now = juliandate.from_gregorian(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
    )

    for i in range(1, 9):
        line = bd.get("semesters", {"id": str(i)})

        if day_now < line[2] and day_now > line[1]:
            semester = line[0]

    lines = bd.get_raw("disciplines", {"semester_id": semester})

    builder = InlineKeyboardBuilder()
    builder.add(
        *[
            InlineKeyboardButton(
                text=item[1].capitalize(), callback_data="dist_" + f"{num}"
            )
            for num, item in enumerate(lines)
        ]
    )

    # Указываем клавиатуру в ответе
    builder.adjust(1)
    await message.answer(
        "Выберете категорию для сохранения", reply_markup=builder.as_markup()
    )
    await message.delete()


@dp.callback_query(F.data.startswith("dist_"))
async def callback(callback):
    global flag, discipline_id

    flag = True
    discipline_id = int(callback.data.split("_")[1]) + 1

    await callback.message.answer(
        "Отправьте сообщение и напишите название, под которым хотите сохранить его."
    )


# Вывод сообщения по категориям
@dp.message(Command("savedfiles"))
async def main(message):

    global chat_id

    chat_id = message.chat.id

    builder = InlineKeyboardBuilder()
    builder.add(
        *[
            InlineKeyboardButton(
                text=str(num).capitalize(), callback_data="sem_" + f"{num}"
            )
            for num in range(1, 9)
        ]
    )

    # Указываем клавиатуру в ответе
    builder.adjust(2)
    await message.answer(
        "Выберете семестр, вы котором хотите найти сохранение",
        reply_markup=builder.as_markup(),
    )
    await message.delete()


@dp.callback_query(F.data.startswith("sem_"))
async def callback(callback):

    semester_id = int(callback.data.split("_")[1])

    bd.start()

    lines = bd.get_raw("disciplines", {"semester_id": semester_id})

    builder = InlineKeyboardBuilder()
    builder.add(
        *[
            InlineKeyboardButton(
                text=item[1].capitalize(), callback_data="dister_" + f"{num}"
            )
            for num, item in enumerate(lines)
        ]
    )
    bd.stop()
    builder.adjust(1)
    await callback.message.answer(
        "Выберете дисциплину, в которой хотите найти сообщение",
        reply_markup=builder.as_markup(),
    )
    await callback.message.delete()


@dp.callback_query(F.data.startswith("dister_"))
async def callback(callback):

    global chat_id

    discipline_id = int(callback.data.split("_")[1]) + 1

    bd.start()

    lines = bd.get_raw("saved", {"discipline_id": discipline_id, "chat_id": chat_id})

    builder = InlineKeyboardBuilder()
    builder.add(
        *[
            InlineKeyboardButton(
                text=item[3].capitalize(), callback_data="name_" + str(item[0])
            )
            for item in lines
        ]
    )
    bd.stop()
    builder.adjust(1)
    await callback.message.answer(
        "Выберете название сохранения",
        reply_markup=builder.as_markup(),
    )
    await callback.message.delete()


# Возвращает сохраненное ранее сообщение, по выбранному названию
@dp.callback_query(F.data.startswith("name_"))
async def callback(callback):
    global chat_id
    message = callback.data.split("_")[1]
    await bot.send_message(
        chat_id=chat_id,
        text="Вот ваше сообщение",
        reply_to_message_id=message,
    )
    await callback.message.delete()


# Перевод из аудио в текст (STT)
@dp.message(F.content_type == ContentType.VOICE)
async def audio(message):
    edittext = ""
    # Download audio file
    file_id = await bot.get_file(message.voice.file_id)
    await bot.download_file(
        file_id.file_path, Path(__file__).parent / "DopClasses" / "audio.ogg"
    )

    # Speech-to-Text convertation
    edittext = STT(Path(__file__).parent / "DopClasses" / "audio.ogg")

    msg = await message.reply(edittext)

    try:
        punctual = STT_whisper(edittext)
        await bot.edit_message_text(
            chat_id=str(message.chat.id), message_id=str(msg.message_id), text=punctual
        )
    except:
        pass


# Очередь для математики
@dp.message(Command("startqueue"))
async def Math(message):
    global members, chat
    members.clear()
    chat = message.chat.id

    await message.answer(
        "Кто хочет участвовать в очереди, напишите любое сообщение. Когда закончите, напишите команду /endqueue"
    )


# Вывод очереди
@dp.message(Command("endqueue"))
async def Math(message):
    global members
    conclusion = ""

    for i in range(len(members)):
        himfirstname = random.choice(list(members.values()))
        conclusion += str(himfirstname) + "\n"
        members = {key: val for key, val in members.items() if val != himfirstname}

    await message.answer("Вот ваша очередь: \n" + conclusion)


# Создание списка людей в группе
@dp.message(F.content_type == ContentType.TEXT)
async def Math(message):
    global members, chat, user_id, flag, discipline_id

    if message.from_user.id == user_id and flag:
        bd.start()

        bd.insert(
            "saved",
            {
                "mes_id": str(message.message_id),
                "chat_id": str(message.chat.id),
                "discipline_id": discipline_id,
                "name": message.text,
            },
        )
        bd.stop()
        flag = False
        await message.answer("Ваше сообщение сохранено")

    bd.start()
    if bd.get("chats", {"id": str(message.chat.id)}) is None:
        bd.insert("chats", {"id": str(message.chat.id), "name": message.chat.title})
    bd.stop()

    if chat == message.chat.id:
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
        "пойдешь?" in message.text.lower().split()
        or "пойдёшь?" in message.text.lower().split()
        or "го?" in message.text.lower().split()
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
