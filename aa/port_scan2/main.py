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

#------------------------------------------------
print('欢迎使用外网端口监测系统V4.0')
print('---------------------------->>>>>>>>>--------\n请在target.txt中设置资产IP+资产端口，格式如下：\n10.10.10.10_80\n--------<<<<<<<<<----------------------------')
print('目前支持扫描方式：1.SYN扫描 2.Telnet扫描')

method = input('请输入扫描方式的序号：')
method = int(method)
# thread_input = input('请输入端口扫描线程：')
# thread_input = int(thread_input)

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
    # 将序号对应的扫描方式函数放入字典中
    methods = {1: scan.syn_portscan, 2: scan.telnet_portscan}
    t_numbers = 0
    threads = []

    # 循环添加扫描线程
    for i in range(1, ports+1):
        print ("线程名称：%s | 当前加载payload： %s" % (url, i))
        # 创建并添加线程， 根据序号使用对应的扫描方式函数
        threads.append(threading.Thread(target=methods[method], args=(url, i)))
        #线程创建数量达到200时执行启动其中的所有线程
        if t_numbers >= 200:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            t_numbers = 0
            threads = []
        t_numbers += 1
    else:
        # 执行余下的所有线程
        if threads:
            for t in threads:
                t.start()
            for t in threads:
                t.join()

threadList = []
for i in open('ip.txt','r'):
    threadList.append(i)

threads = []
threadID = 1

# 创建新线程
for url in threadList:
    thread = myThread(threadID, url, ports=65535)
    threads.append(thread)
    threadID += 1

for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print ("退出主线程")