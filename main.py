from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
import asyncio
from STT import STT, Punct
from messege_bd import data_base as db

# from Schedule import classes
import json
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from threading import Timer

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
/deletesavedfiles - команда для удаления сохранённых сообщений, доступна только админам
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
deletesavedfiles_command = """
Выберете категорию, в которой хотите удалить сохраненные сообщения.
"""
deletecategories_message = """
Выберете название сохранения, которое вы хотите удалить.
"""


# Цикл вызова функции раз в 10 минут
everytenmin = """я получается в первый раз когда использовал это вот сообщение он мне хорошо написал 
все запятые и расставил там потом вот произвести при обновил потому что он просто перестал отвечать 
мне как будто бы первый раз по скорее всего кого-то тоже активирован наверное не знаю и сейчас я снова
открыл вроде бы ставить запятые"""


# Создание бота
bot = Bot(token=main_token)
dp = Dispatcher()

# Создание глобальных переменных
sort = []
categories = []
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


"""# Команда для запуска рассылки напоминаний о расписании
@dp.message(Command("zaprasp"))
async def main(message):
    lessons = classes()
    await message.answer("Расписание запущено")

    await message.answer(lessons)"""


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
    category=category.lower()
    bd.start()
    if category not in categories:
        id_category = bd.get('categories',{'name':"другое"})[0]
        bd.insert('saves',{'mes_id': str(message.message_id), 'chat_id': str(message.chat.id), 'id_category': id_category, 'name': name})
        await message.reply(
            f"Так как еще нет категории <{category}> Ваше сообщение сохранено, в категорию: <Другое>"
        )
    else:
        id_category = bd.get('categories',{'name':category})[0]
        bd.insert('saves',{'mes_id': str(message.message_id), 'chat_id': str(message.chat.id), 'id_category': id_category, 'name': name})
        await message.reply("Ваше сообщение сохранено")
    bd.stop()


# # Команда для удаления сохраненных сообщений, доступнатолько админу
# @dp.message(Command("deletesavedfiles"))
# async def main(message):
#     truefalse = True
#     member = await bot.get_chat_member(message.chat.id, message.from_user.id)
#     for x in member:
#         if "member" in x:
#             truefalse = False
#         break
#     if truefalse == False:
#         await message.answer("Вы не обладаете правами администратора")
#     else:
#         global categories, Admin_ID

#         Admin_ID = message.from_user.id

#         # Инициализируем клавиатуру
#         builder = InlineKeyboardBuilder()

#         builder.add(
#             *[
#                 InlineKeyboardButton(text=item, callback_data="del_" + item)
#                 for item in categories
#             ]
#         )

#         # Указываем клавиатуру в ответе
#         builder.adjust(3)
#         await message.answer(deletesavedfiles_command, reply_markup=builder.as_markup())


# # Вывод сохраненных названий для удаления
# @dp.callback_query(F.data.startswith("del_"))
# async def callback(callback):
#     global sort, action, Admin_ID
#     if callback.from_user.id == Admin_ID:
#         action = callback.data.split("_")[1]
#         builder = InlineKeyboardBuilder()

#         category = filter(lambda x: x["Категория"] == action, sort)
#         builder.add(
#             *[
#                 InlineKeyboardButton(
#                     text=item["Имя"], callback_data="delet_" + item["Message_id"]
#                 )
#                 for item in category
#             ]
#         )

#         builder.adjust(3)
#         await callback.message.answer(
#             deletecategories_message, reply_markup=builder.as_markup()
#         )


# # Удаление сохраненного ранее сообщения
# @dp.callback_query(F.data.startswith("delet_"))
# async def callback(callback):
#     global sort, Admin_ID

#     if callback.from_user.id == Admin_ID:
#         message = callback.data.split("_")[1]

#         category = filter(lambda x: x["Message_id"] == message, sort)

#         for item in category:
#             sort.remove(item)
#         await callback.message.answer("Сохранённое сообщение удалено")


# Вывод сообщения по категориям
@dp.message(Command("savedfiles"))
async def main(message):
    global categories, chat_id
    chat_id = message.chat.id
    # Инициализируем клавиатуру
    builder = InlineKeyboardBuilder()
    builder.add(
        *[
            InlineKeyboardButton(text=item.capitalize(), callback_data="num_" + f'{num}')
            for num, item in enumerate(categories)
        ]
    )

    # Указываем клавиатуру в ответе
    builder.adjust(1)
    await message.answer(savedfiles_command, reply_markup=builder.as_markup())


# Вывод сохраненных названий
@dp.callback_query(F.data.startswith("num_"))
async def callback(callback):
    global action, chat_id
    bd.start()
    action = int(callback.data.split('_')[1])+1
    builder = InlineKeyboardBuilder()

    names = bd.get_raw('saves',{"id_category": action, 'chat_id': chat_id})
    bd.stop()
    builder.add(
        *[
            InlineKeyboardButton(
                text=item[3], callback_data="numm_" + item[0]
            )
            for item in names
        ]
    )

    builder.adjust(3)
    await callback.message.answer(categories_message, reply_markup=builder.as_markup())


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
