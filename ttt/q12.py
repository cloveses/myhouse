import queue
import datetime
import time, random
import threading


businesses = ['存款','取款','挂失','还贷']
business_queues = queue.Queue()
business_spends = [2,3,1,5]
finishes = queue.Queue()
end = datetime.datetime.now() + datetime.timedelta(seconds=20)
end2 = end + datetime.timedelta(seconds=5)

def add_custom(end=end):
    count = 1
    while True:
        business_queues.put((count,random.randint(0,3),datetime.datetime.now()))
        count += 1
        time.sleep(random.randint(0,1))
        # 超时退出线程
        if datetime.datetime.now() > end:
            break

def deal(end=end, end_count=None):
    datas = {}
    while True:
        business = business_queues.get(block=True, timeout=1)
        time.sleep(business[1])
        if business[1] not in datas:
            datas[business[1]] = 1
        else:
            datas[business[1]] += 1
        finishes.put((business[0],business[1],business[2],datetime.datetime.now()))
        # 超时退出线程
        if datetime.datetime.now() > end:
            break
    print('客户总数：', sum(datas.values()))
    print('完成业务类型与数量：')
    for k,v in datas.items():
        print(businesses[k],':',v)
    if end_count:
        end_count()

def end_count():
    number,times = 0,0
    while not finishes.empty():
        b = finishes.get()
        number += 1
        times += (b[-1]-b[-2]).seconds
    print('平均逗留时间：',number/times,"秒")

if __name__ == '__main__':
    # business_queues.join()
    p = threading.Thread(target=add_custom)
    p.start()
    works = [threading.Thread(target=deal),threading.Thread(target=deal),
        threading.Thread(target=deal),threading.Thread(target=deal, args=(end2,end_count))]
    for w in works:
        w.start()
        w.join()
    p.join()
