from multiprocessing import pool
import time, os, random


def aaa(msg):
    t_start = time.time()
    print("%s运行，进程号为%d" % (msg, os.getpid()))
    time.sleep(random.randint(1,3))
    t_stop = time.time()
    print(msg, "已完成，运行时间%0.2f" % (t_stop - t_start))
    return msg

def display(a):
    print(a)
    print('end...')

if __name__ == '__main__':
    po = pool.Pool(3)
    for i in range(0, 3):
        po.apply_async(aaa, args=(i,), callback=display)
    print("----start----")
    po.close()
    po.join()
    print("----stop----")