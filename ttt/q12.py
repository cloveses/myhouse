import queue
import datetime
import time, random
import threading


businesses = ['存款','取款','挂失','还贷']
business_queues = queue.Queue()
business_spends = [2,3,1,5]
finishes = queue.Queue()
end = datetime.datetime.now() + datetime.timedelta(seconds=60*3)

def add_custom():
    count = 1
    while True:
        business_queues.put((count,random.randint(0,3),datetime.datetime.now()))
        count += 1
        time.sleep(random.randint(0,20))
        if datetime.datetime.now() > end:
            break

def deal():
    while True:
        if business_queues.empty():
            time.sleep(1)
            continue
        business = business_queues.get()
        time.sleep(business[1])
        finishes.put((business[0],business[1],business[2],datetime.datetime.now()))
        print(business)
        if datetime.datetime.now() > end:
            break

p = threading.Thread(target=add_custom)
da = threading.Thread(target=deal)
db = threading.Thread(target=deal)
dc = threading.Thread(target=deal)
dd = threading.Thread(target=deal)

p.start()
da.start()
db.start()
dc.start()
dd.start()
print('aaa')