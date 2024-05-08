from messege_bd import db_manager
def create_bone():
    A=db_manager("P3lv1c_bone.db")
    A.start()

    A.create("semesters",{'id':'integer PRIMARY KEY', 'start':'REAL','stop':'REAL'})
    A.create("chats",{"name":"TEXT","id":"integer"})
    A.create("week_days",{'id':'integer primary key','name':'text'})
    A.create("pairs",{'id':'integer','starts':'text'})
    A.create("disciplines",{"id":"integer PRIMARY KEY", "name":'text','semester_id':'integer'},"FOREIGN KEY (semester_id) REFERENCES semesters(id)")
    A.create("saved",{'mes_id':'integer','chat_id':'integer','discipline_id':'integer','name':'text'},"FOREIGN KEY(chat_id) REFERENCES chats(id)",
    "FOREIGN KEY(discipline_id) REFERENCES disciplines(id)")
    A.create("week_disciplines",{'discipline_id':'integer','day_id':'integer','pair_number':'integer'},"FOREIGN KEY (discipline_id) REFERENCES disciplines(id)",
            "FOREIGN KEY(day_id) REFERENCES week_days (id)",
            "FOREIGN KEY(pair_number) REFERENCES pairs(id)"  )

    A.stop()