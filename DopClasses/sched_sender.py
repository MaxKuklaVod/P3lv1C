
from DopClasses.Schedule import weekly_schedule
from DopClasses.messege_bd import db_manager
from pathlib import Path
import sched
import time
import json
import telebot
import asyncio

with open(Path(__file__).parent.parent / "Json" / "login_info.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)

mail_token = tokens["mail"]
password_token=tokens['password']


with open(Path(__file__).parent.parent / "Json" / "tokens.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)

main_token = tokens["test_token"]
bot=telebot.TeleBot(main_token)


scheduler = sched.scheduler(time.time, 
                            time.sleep) 


def send(pair):
    global bot
    bot.send_message('-1002071723643',pair)





#TODO автоматизировать 
def send_schedule():
    
    cur=time.time()
    print(cur)
    db=db_manager("P3lv1c_bone.db")   
    db.start()
    db.delete("week_disciplines",{"day_id":"*"})
    db.stop()
    global mail_token,password_token
    week_sched=weekly_schedule(mail_token,password_token)
    
    # i=cur
    # for cur_day in week_sched:

    #     for cur_pair in week_sched[cur_day]:
    #         i+=120
    #         print(week_sched[cur_day][cur_pair][0])
    #         scheduler.enterabs(i,2, send(week_sched[cur_day][cur_pair][0]))
    # scheduler.enterabs(i+60,2, send_schedule())
    # return scheduler
    #ран

# scheduler=send_schedule()
# scheduler.run()