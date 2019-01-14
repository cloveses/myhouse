# [[学号,姓名,班级,[(时间,状态),..]],]

import pickle
import datetime
import os
import random

stud_status = ['出席','请假','旷课']

def mystart():
    studs = []
    # 数据文件存在则读取并加载到studs列表
    if os.path.exists('dat.db'):
        with open('dat.db','rb') as sf:
            studs = pickle.load(sf)
    #列表中有学生点名记录，则逐条输出
    if studs:
        for stud in studs:
            print(stud[0],stud[1],end=':')
            for d in stud[3]:
                print(d[0],stud_status[d[1]],end=',')
            print()
    # 列表中学生信息为空，则初始化信息（供测试用）
    else:
        # 生成8名测试学生
        for i in range(8):
            studs.append([i+100,''.join([chr(random.randint(97,122)) for i in range(6)]),str(random.randint(1,2)),[]])
    # 获取所有班级编号并显示
    all_classes = list(set([d[2] for d in studs]))
    print('请输入要点名的班级：',all_classes)
    #要求输入点名班级
    stud_class = input()
    if stud_class and stud_class in all_classes:
        print('开始点名（0 出席，1 请假，2 旷课）-------')
        for stud in studs:
            # 如果学生的班级与要点名班级一致则显示
            if stud[2] == stud_class:
                # 循环让用户输入点名状态，错误则重输
                while True:
                    print(stud[0],stud[1],':')
                    data = input()
                    if data and data.isdigit():
                        stud[3].append([datetime.datetime.now(),int(data)])
                        break
                    else:
                        print('输入错误！')
        else:
            # 点名完成，保存点名数据
            with open('dat.db','wb') as sf:
                pickle.dump(studs,sf)
    else:
        print('班级不存在，程序退出！')

# 调用函数，启动程序
mystart()