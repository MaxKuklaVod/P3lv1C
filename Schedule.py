from selenium import webdriver
import datetime
import pytz
import json
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

# need_to_inst
# selenium
# pytz

# Данные для входа
log_info = json.load(open('login_info.json'))

mail = log_info['mail']
password_text = log_info['password']


# Запись расписания в переменную
def classes(mail, password_text):
    # Драйвер для взаимодействия с браузером
    driver = webdriver.Firefox()
    driver.get("https://bki.forlabs.ru/app/login")

    # Процесс входа в систему Forlabs
    login = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[1]/input")
    login.send_keys(mail)

    password = driver.find_element(By.XPATH,"/html/body/div[3]/div/div/form/div/div[2]/center/div/div/div[2]/input")
    password.send_keys(password_text)

    login_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/form/div/div[3]/center/button")
    login_button.click()

    time.sleep(2)

    check_auth_element = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/div[1]/ng-view/div/div/div/div[1]/div/div[1]/div")

    # Переходим на вкладку с расписанием
    driver.get("https://bki.forlabs.ru/app/schedule")
    time.sleep(2)

    # День недели
    current_day = datetime.datetime.today().weekday()

    # Создание словаря для хранения информации о парах
    # schedule - расписание
    schedule = {}

    # Заполнение словаря
    for line_number in range(1, 8):
        # Вывод в воскресенье
        if current_day == 6:
            driver.close()
            return ["Сегодня пар нет", schedule]

        # Проходка по блокам, содержащим время начала занятия и название дисциплины
        try:
            lesson_time = driver.find_element(By.XPATH,f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li/span[1]')
            lesson_name = driver.find_element(By.XPATH,f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(line_number * 7) + current_day + 2}]/ul/li/span[2]/span/a')

            schedule[lesson_time.get_attribute('innerHTML')[0:5]] = lesson_name.get_attribute('innerHTML')
        except NoSuchElementException:
            pass

    driver.close()

    # Время для вычисления следующей пары
    time_zone = pytz.timezone("Asia/Irkutsk")
    current_time = datetime.datetime.now(time_zone).strftime('%H:%M')

    for lesson_time in schedule.keys():
        if current_time < lesson_time:
            result = (f"Следующая пара: {schedule[lesson_time]}, начинается в {lesson_time}")
            return [result, schedule.keys()]
        else:
            pass
    return ["Дальше пар не будет", schedule]


# Функция для повторения отправки сообщения(Ещё не завершена, продумываются другие варианты)
def repeater(func, mail, password):
    res = func(mail, password)
    print(res[0])
    time_zone = pytz.timezone("Asia/Irkutsk")

    starts = ["06:20"]
    starts += res[1]

    for index in enumerate(starts):
        starts[index[0]] = datetime.datetime.strptime(starts[index[0]], "%H:%M").time()
        starts[index[0]] = str(datetime.timedelta(hours=starts[index[0]].hour, minutes=starts[index[0]].minute) - datetime.timedelta(
            minutes=20)).replace(":", "")
        if len(starts[index[0]]) < 6:
            starts[index[0]] = "0" + starts[index[0]]

    while True:
        current_time = str(datetime.datetime.now(time_zone).strftime("%H:%M:%S")).replace(":", "")
        if current_time in starts:
            repeater(func, mail, password)


repeater(classes,mail,password_text)