import pytz
import json
import asyncio
import datetime
import time
from pathlib import Path
from aiogram import Bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from apscheduler.triggers.cron import CronTrigger
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# Код для запуска функции, повторяющей вызов расписания
"""
scheduler = AsyncIOScheduler()
scheduler.add_job(check_schedule, CronTrigger(hour='6-18', minute='0', second='0'),args=[mail_text,password_text,chat_id])
scheduler.start()

asyncio.run(check_schedule(mail_text, password_text, chat_id))
"""

# Библиотеки, требующие установки
"""
selenium
apscheduler
"""


async def daily_classes(mail_arg, password_arg,day):
    '''
    На вход: логин, пароль
    Возвращает: словарь(ключи - время начала пары, значения - название и место проведения пары)
    '''

    # Запуск браузера
    opt = Options()
    opt.add_argument("--headless")
    driver = webdriver.Firefox(options=opt)
    driver.get("https://bki.forlabs.ru/app/login")

    # Ожидание элементов авторизации
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[1]/input")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[2]/input")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/form/div/div[3]/center/button")))

    # Ввод логина и пароля, вход в аккаунт
    login = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[1]/input")
    login.send_keys(mail_arg)

    password = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[2]/input")
    password.send_keys(password_arg)

    login_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[3]/center/button")
    login_button.click()

    await asyncio.sleep(1)

    # Переход на страницу с расписанием
    driver.get("https://bki.forlabs.ru/app/schedule")

    current_day = day
    schedule = {}

    await asyncio.sleep(2)


    # Заполнение словаря с парами
    for line_number in range(1, 8):
        if current_day == 6:
            driver.close()

        # Поиск названия, времени и места проведения пары
        try:
            lesson_name = driver.find_element(By.XPATH,
                                              f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li/span[2]/span/a')
            lesson_place = driver.find_element(By.XPATH,
                                               f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li[1]/span[5]')

            schedule[line_number] = [lesson_name.get_attribute('innerHTML'),lesson_place.get_attribute('innerHTML')]

        # Исключение, срабатывающее при ненахождении элемента
        except NoSuchElementException:
            pass

    driver.close()

    time_zone = pytz.timezone("Asia/Irkutsk")
    current_time = datetime.datetime.now(time_zone).strftime('%H:%M')

    # Возвращение сообщения
    if schedule != {}:
        return schedule


# Функция для получения списка предметов в семестре
async def list_of_classes(mail_arg, password_arg):
    '''
    На вход: логин и пароль
    Возвращает: массив названий предметов в семестре
    '''

    # Создание массива для хранения названий предметов
    classes_list = []

    # Запуск браузера
    opt = Options()
    opt.add_argument("--headless")
    driver = webdriver.Firefox(options=opt)
    driver.get("https://bki.forlabs.ru/app/login")

    # Ожидание элементов авторизации
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[1]/input")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[2]/input")))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/form/div/div[3]/center/button")))

    # Ввод логина и пароля, вход в аккаунт
    login = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[1]/input")
    login.send_keys(mail_arg)

    password = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[2]/input")
    password.send_keys(password_arg)

    login_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[3]/center/button")
    login_button.click()

    await asyncio.sleep(1)

    # Переход на вкладку со списком предметов
    driver.get("https://bki.forlabs.ru/app/learning/187/studies")

    await asyncio.sleep(2)

    # Заполнение массива с названиями предметов
    line = 1
    while True:
        try:
            subject = driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div[2]/div[2]/div/div/table/tbody/tr[{line}]/td[1]/a")
            classes_list.append(subject.get_attribute("innerHTML"))
            line += 1
        except NoSuchElementException:
            driver.close()
            return classes_list


async def weekly_schedule(mail_arg,password_arg):
    # Создание словаря для хранения расписания по дням
    weekly_classes = {}

    day_subjects = None
    for day in range(0,6):
        try:
            day_subjects = daily_classes(mail_arg,password_arg,day)
        except NoSuchElementException:
            pass
        if day_subjects is not None:
            weekly_classes[day+1] = day_subjects
    if weekly_classes != {}:
        return weekly_classes


# async def check_schedule(mail_arg,password_arg,chat_id):
#     with open(Path(__file__).parent.parent / "Json" / "tokens.json", encoding="utf-8") as complex_data:
#             data = complex_data.read()
#             tokens = json.loads(data)
#     channel=tokens['group']
#     main_token = tokens["test_token"]
#     bot=Bot(token=main_token)
#     while True:
#         job_result = await daily_classes(mail_arg, password_arg)
#         if job_result is not None:
#             await bot.send_message(chat_id=channel, text=job_result)
#         await asyncio.sleep(5400)  # Таймер на 1.5 часа
