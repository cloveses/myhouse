import queue
import datetime
import time, random
import threading


mutex = threading.Lock()
businesses = ['存款','取款','挂失','还贷']
business_queues = queue.Queue()
business_spends = [5,8,7,9]
finishes = queue.Queue()
end = datetime.datetime.now() + datetime.timedelta(seconds=20)
end2 = end + datetime.timedelta(seconds=5)

def add_custom():
    count = 1
    while True:
        business_queues.put((count,random.randint(0,3),datetime.datetime.now()))
        count += 1
        time.sleep(random.randint(0,1))
        # 超时退出线程
        print(threading.currentThread().getName(),'working....')
        if datetime.datetime.now() > end:
            print(threading.currentThread().getName(),'exit....')
            break

def deal():
    datas = {}
    while True:
        print(threading.currentThread().getName(),'working....')
        if business_queues.empty():
            time.sleep(random.randint(1,5))
        mutex.acquire()
        if business_queues.qsize() != 0:
            business = business_queues.get()#block=True, timeout=1
            mutex.release()
            time.sleep(business[1])
            if business[1] not in datas:
                datas[business[1]] = 1
            else:
                datas[business[1]] += 1
            finishes.put((business[0],business[1],business[2],datetime.datetime.now()))
        else:
            mutex.release()
        # 超时退出线程
        if datetime.datetime.now() > end2:
            print(threading.currentThread().getName(),'exit....')
            break
    print()
    print('客户总数：', sum(datas.values()))
    print('完成业务类型与数量：')
    for k,v in datas.items():
        print(businesses[k],':',v)

def end_count():
    number,times = 0,0
    while not finishes.empty():
        b = finishes.get()
        number += 1
        times += (b[-1]-b[-2]).seconds
    print()
    print('平均逗留时间：',number/times,"秒")

if __name__ == '__main__':
    p = threading.Thread(target=add_custom)
    p.start()
    works = [threading.Thread(target=deal),threading.Thread(target=deal),
        threading.Thread(target=deal),threading.Thread(target=deal)]
    for w in works:
        w.start()
    # 让所有子线程结束后统计
    for w in works:
        w.join()
    end_count()