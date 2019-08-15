# -*- coding:UTF-8 -*-
#*********************************************
#------->>>>>>Author:秋某人的傻逼                    *
#------->>>>>>Name:熊猫最爱皮卡丘                        *
#------->>>>>>Target:端口实时监控工具V4.0代码重构版本  *
#*********************************************

#--------------------/工具编写思路/--------------------
#1.设置需要监控的IP地址和端口
#2.扫描IP端口（扫描进行优化），与默认端口进行对比，如果有异常即发送邮件
#3.
#4.
#--------------------/工具编写思路/--------------------
import scan
import queue
import threading
import time
import random

scan.syn_portscan('127.0.0.1', 1234)

#------------------------------------------------
print('欢迎使用外网端口监测系统V4.0')
print('---------------------------->>>>>>>>>--------\n请在target.txt中设置资产IP+资产端口，格式如下：\n10.10.10.10_80\n--------<<<<<<<<<----------------------------')
print('目前支持扫描方式：1.SYN扫描 2.Telnet扫描')

method = input('请输入扫描方式的序号：')
method = int(method)
thread_input = input('请输入端口扫描线程：')
thread_input = int(thread_input)

queueLock = threading.Lock()


class myThread (threading.Thread):
    def __init__(self, threadID, url, ports):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.ports = ports

    def run(self):
        time.sleep(random.randint(1,4))
        print ("开启线程：" + self.url)
        goscan(self.url, self.ports , method)
        print ("退出线程：" + self.url)

def goscan(url, ports ,method):
    while not ports.empty():
        try:
            queueLock.acquire()
            port = ports.get()
            print ("线程名称：%s | 当前加载payload： %s" % (url, port))
            if method == 1:
                scan.syn_portscan(url, port)
            elif method == 2:
                scan.telnet_portscan(url, port)
        finally:
            queueLock.release()
        time.sleep(random.randint(1,2))


threadList = []
for i in open('ip.txt','r'):
    threadList.append(i)

workQueue = queue.Queue(65535)
# 填充队列
for port in range(1,65535):
    workQueue.put(port)

threads = []
threadID = 1

# 创建新线程
for url in threadList:
    thread = myThread(threadID, url, workQueue)
    threads.append(thread)
    threadID += 1

for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print ("退出主线程")