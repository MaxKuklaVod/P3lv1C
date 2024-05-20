from DopClasses.messege_bd import db_manager



def save_schedule(week_disciplines:dict)->None:
    db=db_manager("P3lv1c_bone.db")   
    db.start()
    for cur_day in week_disciplines:

        for cur_discipline in week_disciplines[cur_day]:

            db.insert("week_disciplines",{"discipline_name":str(week_disciplines[cur_day][cur_discipline][0]),"day_id":str(cur_day),"pair_number":str(cur_discipline)})