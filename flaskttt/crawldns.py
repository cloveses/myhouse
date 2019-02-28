import requests
import json
import time
from bs4 import BeautifulSoup
import threading
import pandas as pd
import pymysql
import signal


# 多线程爬域名信息
# threadNum是线程数，可以修改的
#
class calThread(threading.Thread):

    def __init__(self, index, data, perlen, resultFile):

        threading.Thread.__init__(self)

        self.index = index

        self.data = data

        self.perlen = perlen

        self.resultFile = resultFile

        self.stop = False

    def handler(self, s, f):

        self.stop = True

    def run(self):

        crawl_yuming = self.data[self.index * self.perlen:(self.index + 1) * self.perlen]  # 设定每个线程的运行数据范围，以免重复采

        # 不同的域名分情况考虑，但都包括了所有的情况
        for per in crawl_yuming:

            if self.stop:

                break

            title = ""

            print(per)

            per = per.strip('\n')  # 去除换行符

            # web_url ="http://www.dnjbuilders.com"
            try:

                web_url = "https://www." + per

                html = requests.get(url=web_url, timeout=50)  # timeout可以自己设定

                html.encoding = html.apparent_encoding  # 处理网页乱码问题

                soup = BeautifulSoup(html.text, "html.parser")  # 解析网页

                title = soup.find("title").getText()  # 根据标签找到title


            except:

                try:

                    web_url = "http://www." + per

                    html = requests.get(url=web_url, timeout=50)

                    html.encoding = html.apparent_encoding

                    soup = BeautifulSoup(html.text, "html.parser")

                    if title == None:
                        title = soup.find("title").getText()


                except:

                    if title == None:
                                title = None




            row = {"domainName": per, "title": title}  # 一条数据

            print(row)

            self.resultFile[per] = row  # 放入字典里


if __name__ == "__main__":

    thread_list = []

    resultFile = {}

    threadNum = 100 # 线程数可以自定义

    # result = pd.DataFrame(columns=['domainName','title'])

    file = open("list3.txt")  # 读取文件

    data = []

    for s in file:
        data.append(s)


    per_len = int(len(data) / threadNum)  # 为了使得每个线程有爬不同的数据

    for i in range(threadNum):

        new_thread = calThread(i, data, per_len, resultFile)

        signal.signal(signal.SIGTSTP, new_thread.handler)

        thread_list.append(new_thread)  # 线程

        new_thread.start()

    for thread in thread_list:
        
        thread.join()

    connect = pymysql.Connect(host="localhost", port=3306, user="root", passwd="", database="domaininfo",
                              charset='utf8')  # 连接数据库

    cursor = connect.cursor()  # 获取游标

    sql = "INSERT INTO domain_info(domainName,title) VALUES (%s,%s)"  # 插入数据的sql语句

    for s, v in resultFile.items():  # 批量插入

        connect.ping(reconnect=True)

        cursor.execute(sql, (v['domainName'], v['title']))

        connect.commit()  # 提交事务
        connect.close()  # 关闭数据连接

