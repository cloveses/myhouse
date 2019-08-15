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

#------------------------------------------------
print('欢迎使用外网端口监测系统V4.0')
print('---------------------------->>>>>>>>>--------\n请在target.txt中设置资产IP+资产端口，格式如下：\n10.10.10.10_80\n--------<<<<<<<<<----------------------------')
print('目前支持扫描方式：1.SYN扫描 2.Telnet扫描')

exitFlag = 0

method = input('请输入扫描方式的序号：')
method = int(method)
thread_input = input('请输入端口扫描线程：')
thread_input = int(thread_input)


class myThread (threading.Thread):
    def __init__(self, threadID, url, ports):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.ports = ports
    def run(self):
        print ("开启线程：" + self.url)
        goscan(self.url, self.ports , method)
        print ("退出线程：" + self.url)

def goscan(url, ports ,method):
    if method == 1:
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                port = ports.get()
                queueLock.release()
                print ("线程名称：%s | 当前加载payload： %s" % (url, port))
                scan.syn_portscan(url, port)
            else:
                queueLock.release()
            time.sleep(1)
    elif method == 2:
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                port = ports.get()
                queueLock.release()
                print ("线程名称：%s | 当前加载payload： %s" % (url, port))
                scan.telnet_portscan(url, port)
            else:
                queueLock.release()
            time.sleep(1)
threadList = []
for i in open('ip.txt','r'):
    threadList.append(i)
queueLock = threading.Lock()
workQueue = queue.Queue(thread_input)
threads = []
threadID = 1

# 创建新线程
for url in threadList:
    thread = myThread(threadID, url, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for port in range(1,65535):
    workQueue.put(port)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")