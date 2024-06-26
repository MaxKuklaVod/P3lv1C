from messege_bd import db_manager


def create_bone():
    A = db_manager("P3lv1c_bone.db")
    A.start()

    A.create(
        "semesters", {"id": "integer PRIMARY KEY", "start": "REAL", "stop": "REAL"}
    )
    A.create("chats", {"name": "TEXT", "id": "integer"})
    A.create("week_days", {"id": "integer primary key", "name": "text"})
    A.create("pairs", {"id": "integer", "starts": "text"})
    A.create(
        "disciplines",
        {"id": "integer PRIMARY KEY", "name": "text", "semester_id": "integer"},
        "FOREIGN KEY (semester_id) REFERENCES semesters(id)",
    )
    A.create(
        "saved",
        {
            "mes_id": "integer",
            "chat_id": "integer",
            "discipline_id": "integer",
            "name": "text",
        },
        "FOREIGN KEY(chat_id) REFERENCES chats(id)",
        "FOREIGN KEY(discipline_id) REFERENCES disciplines(id)",
    )
    A.create(
        "week_disciplines",
        {"discipline_name": "text", "day_id": "integer", "pair_number": "integer"},
        "FOREIGN KEY(day_id) REFERENCES week_days (id)",
        "FOREIGN KEY(pair_number) REFERENCES pairs(id)",
    )

    # чётные - 8 июля, нечётные - 25 января
    dates = [
        "2460189",
        "2460335",
        "2460511",
        "2460701",
        "2460865",
        "2461066",
        "2460865",
        "2461431",
        "2461595",
    ]
    for index in range(len(dates) - 1):

        A.insert(
            "semesters",
            {
                "id": f"{index+1}",
                "start": f"{float(dates[index])}",
                "stop": f"{float(dates[index+1])}",
            },
        )
    courses = {
        1: [
            "Физическая культура и спорт",
            "Безопасность жизнидеятельности",
            "Математика",
            "Информатика",
            "Программирование",
            "Дискретная Математика",
            "Основы российской государственности",
            "Языки разметки сетевого контента",
            "Деловой (проффесиональный) английский язык",
        ],
        2: [
            "Русский язык и культура речи",
            "Иностранный язык",
            "Физическая культура и спорт",
            "Информационные системы и технологии",
            "Объектно-ориентированный анализ и программирование",
            "Компьютерное зрение",
            "Шаблоны проектирования",
        ],
        3: [
            "Иностранный язык",
            "Экономическая культура и основы финансовой грамотности",
            "Теория вероятностей и математическая статистика" "Операционные системы",
            "Культура разработки програмного обеспечения с открытым исходным кодом",
            "Прикладная математика",
            "Анализ данных и машинное обучение",
            "Веб-программирование на стороне клиента",
            "Элективные дисциплины, (модули) по физической культуре",
        ],
        4: [
            "Управление проектами",
            "Иностранный язык",
            "Базы данных",
            "Культура разработки програмного обеспечения с открытым исходным кодом",
            "Нейронные сети и обработка текста",
            "Нейронные сети и компьютерное зрение",
            "Веб-программирование",
            "Юзабилити и дизайн интерфейсов",
            "Элективные дисциплины, (модули) по физической культуре",
        ],
        5: [
            "История России",
            "Экономика",
            "Вычислительные системы и компьютерные сети",
            "Теория и практика языков программирования",
            "Основы мобильной разработки",
            "Практикум по разработки интерфейсов",
            "Интернет вещей",
            "Технологии создания и отладки сценариев интерактивного контента",
            "Алгоритмы на графах",
            "Адаптивные информационные технологии",
            "Интеллектуальные агенты, графовые сети и другие задачи машинного обучения",
            "Трёхмерное графическое моделирование и анимация",
            "Проектное обучение",
            "Элективные дисциплины, (модули) по физической культуре",
        ],
        6: [
            "Основы научно-исследовательской деятельности",
            "История России",
            "Вычислительные системы и компьютерные сети",
            "Информационная безопасность",
            "Инфографика и визуализация данных",
            "Интернет вещей",
            "Экономика и управление технологическими стартапами",
            "Курсовая работа",
            "Интеллектуальные агенты, графовые сети и другие задачи машинного обучения",
            "Трёхмерное графическое моделирование и анимация",
            "Разработка приложений для мобильных устройств",
            "Системы компьютерной математики",
            "Гейм-дизайн",
            "Проектное обучение",
            "Элективные дисциплины, (модули) по физической культуре",
        ],
        7: [
            "Психология социального взаимодействия, саморазвития и самоорганизации",
            "Философия",
            "Стандартизация, сертификация, и управление качеством програмного обеспечения",
            "Управление ИТ-сервисами и контентом",
            "Проектирование информационных систем",
            "Разработка компьютерных игр",
            "Инженерия знаний и интеллектуальные системы",
            "Разработка приложений дополненной реальности",
            "Психология личности и профессиональное самоопределение",
            "Основы разработки прикладных решений 1С-Предприятие",
            "Разработка приложений виртуальной реальности",
            "Элективные дисциплины, (модули) по физической культуре",
        ],
        8: ["проект"],
    }
    id = 1
    for cur_key in list(courses.keys()):
        for cur_dis in courses[cur_key]:
            A.insert(
                "disciplines",
                {"id": str(id), "name": cur_dis, "semester_id": str(cur_key)},
            )
            id += 1
    week_days = {
        1: "Понедельник",
        2: "Вторник",
        3: "Среда",
        4: "Четверг",
        5: "Пятница",
        6: "Суббота",
        7: "Воскресенье",
    }
    for cur_id in list(week_days.keys()):
        A.insert("week_days", {"id": str(cur_id), "name": week_days[cur_id]})

    pairs = {
        1: "3:30",
        2: "5:10",
        3: "6:50",
        4: "8:50",
        5: "10:30",
        6: "12:10",
        7: "13:50",
    }
    for cur_id in list(pairs.keys()):
        print(cur_id)
        A.insert("pairs", {"id": str(cur_id), "starts": pairs[cur_id]})

    A.stop()


create_bone()