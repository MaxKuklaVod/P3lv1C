
from DopClasses.Schedule import weekly_schedule
from pathlib import Path
import sched
import time
import json
import asyncio

with open(Path(__file__).parent.parent / "Json" / "login_info.json") as complex_data:
    data = complex_data.read()
    tokens = json.loads(data)

mail_token = tokens["mail"]
password_token=tokens['password']
scheduler = sched.scheduler(time.time, 
                            time.sleep) 


async def send(bot,pair):
    await bot.send_message('-1002071723643',pair)

def send_schedule(bot):
    global mail_token,password_token
    week_sched=weekly_schedule(mail_token,password_token)
    
    i=0
    for cur_day in week_sched:

        for cur_pair in week_sched[cur_day]:
            i+=7
            scheduler.enter(i+5,2, lambda: asyncio.run(send(bot,week_sched[cur_day][cur_pair][0])))
    scheduler.run()
    #ран