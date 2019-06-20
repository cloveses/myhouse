# -*- coding:UTF-8 -*-
#*********************************************##########################        #############
#------->>>>>>Author:秋某人的傻逼                    *#############     ###    ##     #########
#------->>>>>>Name:熊猫最爱皮卡丘                         *##########      ####     #########
#------->>>>>>Target:批量TCP-ping软件V1.0             *################           #########
#*********************************************############################    #########
#####################################################################################



import re
import datetime
import sys
import os
import threading
import os

class myThread (threading.Thread):
    def __init__(self, threadID, name, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip = ip

    def run(self):
        print ("开启线程： " + self.name)
        # 获取锁，用于线程同步
        # threadLock.acquire()
        btch_p = Btch_P(self.ip)
        btch_p.batch_ping()
        # 释放锁，开启下一个线程
        # threadLock.release()

class Btch_P:
    def __init__(self,ip):
        self.ip = ip

    def batch_ping(self):
        print('开始')
        dirpath = 'result/'
        # 判断路径是否存在，然后判断文件是否存在，如果存在就将文件删除，如果路径不存在就创建目录
        if os.path.exists('result'):
            if os.listdir('result'):
                print('文件夹Ports已经存在，正在对文件进行清空...')
                for file in os.walk('result'):
                    print('os.walk返回对象' + str(file))
                    for items in file[2]:
                        print('目标文件：' + items)
                        os.remove(dirpath + items)
                        print(items + '| 文件已删除')
            else:
                print('result目录已经存在，且无文件！')
        else:
            os.mkdir('result')
            print('Ports目录生成成功！')

        cmd2 = 'ping %s -n 2' % (self.ip)
        res = os.popen(cmd2)
        ssping = res.read()

        pingIp2 = re.compile(r'来自..+', re.M).findall(ssping)  # 通过正则表达式筛选出需要的哪一行
        now = datetime.datetime.now()
        path = 'ping_result/'
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            os.makedirs(path)
            print(path + ' 创建成功')
        else:
            print(path + ' 目录已存在')
        print('写入文件')
        with open('ping_result/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '__' + self.ip.replace('.','_')+ '.txt','a+') as f:
            f.write('ip地址是：' + self.ip + '时间是：'+ str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_' + str(now.minute) + '结果是：' + '\n' +str(pingIp2) + '\n')
            f.close()

def batch_ping_main(ip):
    print(ip)
    threads = []
    # 创建新线程
    for i in range(3):
        threads.append(myThread(i, "Thread-{}".format(i), ip))

    for t in threads:
        t.start()

    # for t in threads:
    #     t.join()
    threads[-1].join()
    print ("退出主线程")

if __name__ == "__main__":
    ip = sys.argv[1]
    threads = []
    # 创建新线程
    for i in range(3):
        threads.append(myThread(i, "Thread-{}".format(i), ip))

    for t in threads:
        t.start()

    # for t in threads:
    #     t.join()
    threads[-1].join()
    print ("退出主线程")
