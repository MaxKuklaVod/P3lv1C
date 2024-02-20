import pytz
import json
import asyncio
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from selenium.common.exceptions import NoSuchElementException

# Импорт данных
log_info = json.load(open('login_info.json'))

mail = log_info['mail']
password_text = log_info['password']

async def classes():
    # Запуск браузера
    driver = webdriver.Firefox()
    driver.get("https://bki.forlabs.ru/app/login")

    # Ввод логина и пароля, вход в аккаунт
    login = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[1]/input")
    login.send_keys(mail)

    password = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[2]/input")
    password.send_keys(password_text)

    login_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[3]/center/button")
    login_button.click()

    await asyncio.sleep(2)

    # Переход на страницу с расписанием
    driver.get("https://bki.forlabs.ru/app/schedule")
    await asyncio.sleep(2)

    current_day = datetime.datetime.today().weekday()
    schedule = {}

    # Заполнение словаря с парами
    for line_number in range(1, 8):
        if current_day == 6:
            driver.close()

        # Поиск названия, времени и места проведения пары
        try:
            lesson_time = driver.find_element(By.XPATH,
                                              f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li/span[1]')
            lesson_name = driver.find_element(By.XPATH,
                                              f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li/span[2]/span/a')
            lesson_place = driver.find_element(By.XPATH,
                                               f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li[1]/span[5]')

            schedule[lesson_time.get_attribute('innerHTML')[0:5]] = [lesson_name.get_attribute('innerHTML'),lesson_place.get_attribute('innerHTML')]

        # Исключение, срабатывающее при ненахождении элемента
        except NoSuchElementException:
            pass

    driver.close()

    time_zone = pytz.timezone("Asia/Irkutsk")
    current_time = datetime.datetime.now(time_zone).strftime('%H:%M')

    # Возвращение сообщения
    for lesson_time in schedule.keys():
        if current_time < lesson_time:
            result = (f"Следующая пара: {schedule[lesson_time][0]}, начинается в {lesson_time} в {schedule[lesson_time][1]}")
            return result
        else:
            pass



# Функция-планировщик
async def schedule_classes(job):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, trigger='interval', hours=1.5, start_date=datetime.datetime.now().replace(hour=6, minute=30, second=0), end_date=datetime.datetime.now().replace(hour=18, minute=0, second=0))
    scheduler.start()

    while True:
        await asyncio.sleep(3600)  # Проверяем каждый час


# Тест
asyncio.run(schedule_classes(classes))
