import datetime
from DopClasses.messege_bd import db_manager
from zoneinfo import ZoneInfo

bd = db_manager("P3lv1c_bone.db")
bd.start()
pairs=[]
for i in range (8):
    pairs.append(bd.get("pairs",{'id':f'{i+1}'}))

"""day_id": "integer", "pair_number": "integer"""

def get_number():
    global pairs
    pair_ranges_by_numbers={}
    for cur_num in pairs:
        if cur_num is not None:
            number,time=cur_num
            hour,mins=time.split(':')
            mins=int(mins)+30
            hour=int(hour)+1+1*(mins//60>0)
            mins%=60
            pair_ranges_by_numbers[number]=(time,f'{hour}:{mins}')
    return pair_ranges_by_numbers

def get_pair_name(day,number):
    return bd.get("week_disciplines",{"day_id":str(day),"pair_number":str(number)})


def get_pair():
    global pairs
    #cur_time=datetime.datetime.strptime("21-05-2024/11:41",'%d-%m-%Y/%H:%M')
    cur_time=datetime.datetime.now(tz=ZoneInfo('Europe/Moscow'))

    
    
    pair_ranges_by_numbers=get_number()

    pair=None

    day=cur_time.weekday()+1
    date_str=cur_time.strftime('%d-%m-%Y')
    time_str=cur_time.strftime('%H:%M')

    cur_time=datetime.datetime.strptime(date_str+'/'+time_str,'%d-%m-%Y/%H:%M')
    print(cur_time)
    for cur_pair in range(1,8):
        start=datetime.datetime.strptime(date_str+'/'+pair_ranges_by_numbers[cur_pair][0],'%d-%m-%Y/%H:%M')
        finish=datetime.datetime.strptime(date_str+'/'+pair_ranges_by_numbers[cur_pair][1],'%d-%m-%Y/%H:%M')
        if cur_time<=finish:
            pair=cur_pair
            break
    return get_pair_name(day,pair)

print(get_pair())
