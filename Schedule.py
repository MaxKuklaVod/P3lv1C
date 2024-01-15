from selenium import webdriver
from forlabs import mail, password_text
import datetime
import pytz
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

# need_to_inst
# selenium
# pytz

# Данные для входа
mail = mail
password_text = password_text
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

    check_auth_element = False

    while not check_auth_element:
        try:
            check_auth_element = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[2]/div[1]/ng-view/div/div/div/div[1]/div/div[1]/div")
        except NoSuchElementException:
            pass

    # Переходим на вкладку с расписанием
    driver.get("https://bki.forlabs.ru/app/schedule")
    time.sleep(3)


    # День недели
    current_day = datetime.datetime.today().weekday() + 1

    # Создание словаря для хранения информации о парах
    schedule = {}

    # Заполнение словаря
    if current_day in range(1, 7):
        for period in range(1, 8):
            lesson_time = False

            while not lesson_time:
                try:
                    lesson_time = driver.find_element(By.XPATH,f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(period * 7) + current_day + 1}]/ul/li/span[1]')
                    lesson_name = driver.find_element(By.XPATH,f'/html/body/div/div[3]/div[2]/div[1]/ng-view/div[2]/div/div/div[2]/div[{(period * 7) + current_day + 1}]/ul/li/span[2]/span/a')

                    schedule[lesson_time.get_attribute('innerHTML')[0:5]] = lesson_name.get_attribute('innerHTML')
                except NoSuchElementException:
                    break

    driver.close()

    # Время для вычисления следующей пары
    time_zone = pytz.timezone("Asia/Irkutsk")
    current_time = datetime.datetime.now(time_zone).strftime('%H:%M')

    lessons_count = len(schedule)

    for t in schedule.keys():
        if current_time < t and lessons_count > 0:
            result = (f"Следующая пара: {schedule[t]}, начинается в {t}")
            return [result, schedule.keys()]
        else:
            pass
    return ["Дальше пар не будет", schedule]

def repeater(func, mail, password):
    res = func(mail, password)
    print(res[0])
    time_zone = pytz.timezone("Asia/Irkutsk")

    starts = ["06:20"]
    starts.extend(res[1])

    for i in range(len(starts)):
        starts[i] = datetime.datetime.strptime(starts[i], "%H:%M").time()
        starts[i] = str(datetime.timedelta(hours=starts[i].hour, minutes=starts[i].minute) - datetime.timedelta(minutes = 20)).replace(":","")
        if len(starts[i]) < 6:
            starts[i] = "0" + starts[i]

    while True:
        current_time = str(datetime.datetime.now(time_zone).strftime("%H:%M:%S")).replace(":", "")
        if current_time in starts:
            repeater(func,mail,password)


repeater(classes,mail,password_text)


