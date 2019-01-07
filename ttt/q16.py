# 文件中数据
# idcode name 点名时间 状态 点名时间 状态...

import datetime
import pickle
import random

STATUS = ['缺席','正常','请假']

class Student:

    def __init__(self, idcode, name, mclass):
        self.idcode = idcode
        self.name = name
        self.mclass = mclass
        self.datas = []

    def display(self):
        print('学号：', self.idcode)
        print('姓名：', self.name)
        for date,status in self.datas:
            print(date.year,date.month,date.day,date.hour,date.minute,STATUS[status])

    def add_status(self, date, status):
        self.datas.append((date,status))

def init():
    datas = []
    for i in range(1,9):
        mclass = random.randint(1,2)
        name = ''.join([chr(random.randint(97,125)) for i in range(5)])
        datas.append(Student(i,name,mclass))
    with open('stud.db','wb') as f:
        pickle.dump(datas,f)

def load():
    with open('stud.db','rb') as f:
        datas = pickle.load(f)
    for s in datas:
        s.display()
    return datas

def main():
    datas = load()
    mclasses = set((d.mclass for d in datas))
    print('当前所有班级：', mclasses)
    while True:
        mclass = input('点名班级：')
        if mclass.isdigit():
            mclass = int(mclass)
            if mclass in mclasses:
                break
    



