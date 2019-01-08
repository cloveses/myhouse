# 文件中数据
# idcode name 点名时间 状态 点名时间 状态...

import datetime
import pickle
import random
import os

STATUS = ['缺席','正常','请假']

class Student:

    def __init__(self, idcode, name, mclass):
        self.idcode = idcode
        self.name = name
        self.mclass = mclass
        self.datas = []

    def display(self):
        print('班级','学号', '姓名',)
        print(self.mclass,self.idcode,self.name,end=' ')
        for date,status in self.datas:
            print(datetime.datetime.isoformat(date) ,STATUS[status],end='\t')
        print()

    def add_status(self, date, status):
        self.datas.append((date,status))

# 初始化测试数据
def init():
    datas = []
    for i in range(1,9):
        mclass = random.randint(1,2)
        name = ''.join([chr(random.randint(97,122)) for i in range(5)])
        datas.append(Student(i,name,mclass))
    with open('stud.db','wb') as f:
        pickle.dump(datas,f)

def load():
    with open('stud.db','rb') as f:
        datas = pickle.load(f)
    for s in datas:
        s.display()
    return datas

def save(datas):
    if datas:
        with open('stud.db','wb') as f:
            pickle.dump(datas,f)

def main():
    # 载入数据
    datas = load()
    # 获取所有班级
    mclasses = set((d.mclass for d in datas))
    print('当前所有班级：', ','.join([str(c) for c in mclasses]))
    # 选择点名班级
    while True:
        mclass = input('点名班级：')
        if mclass.isdigit():
            mclass = int(mclass)
            if mclass in mclasses:
                break
    studs = [s for s in datas if s.mclass==mclass]
    others = [s for s in datas if s.mclass!=mclass]
    studs.sort(key=lambda s:s.idcode)
    print('----------------')
    print('开始点名……')
    print('回车表示出席，0表示缺席，2表示请假。')
    print('----------------')
    date = datetime.datetime.now()
    for stud in studs:
        print(stud.idcode,stud.name,':',end='')
        while True:
            status = input()
            if status == "":
                status = 1
                break
            elif status.isdigit() and int(status) in (0,2):
                status = int(status)
                break
            else:
                print('输入错误，请重新输入：')
        stud.datas.append((date,status))
    others.extend(studs)
    save(others)

if __name__ == '__main__':
    if not os.path.exists('stud.db'):
        init()
    main()

