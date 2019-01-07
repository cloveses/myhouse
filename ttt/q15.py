# [(datetime,duration):False,...]

import datetime

def init():
    datas = {}
    td = datetime.date.today()
    for i in range(7):
        for j in range(6):
            for k in range(1,21):
                datas[(datetime.datetime(td.year, td.month, td.day,8 + j * 2,0,0) + datetime.timedelta(days=i),k)] = False

    # print(datas)
    return datas

def query(datas):
    input_info = input('请输入年月日、时间段开始点及机位号(2019,1,8,10,3):')
    input_info = [i for i in input_info.split(',')]
    if (not all([i.isdigit() for i in input_info])) or len(input_info) != 5:
        print('输入信息有误，请按格式输入：')
        return
    input_info = [int(i) for i in input_info]
    position = input_info[-1]
    if input_info[-2] % 2 != 0 or input_info[-2] < 8 or input_info[-2] >20:
        print('时间信息有误，8－20')
        return
    year,month,day,start = input_info[:4]
    date = datetime.datetime(year,month,day,start,0,0)
    if datas[(date,position)]:
        print(date,'已占用！')
    else:
        print(date,'未占用！')

# 登记预订
def reg(datas,waiter):
    input_info = input('请输入年月日、时间段开始点及机位号(2019,1,8,10,3):')
    input_info = [i for i in input_info.split(',')]
    if (not all([i.isdigit() for i in input_info])) or len(input_info) != 5:
        print('输入信息有误，请按格式输入：')
        return
    input_info = [int(i) for i in input_info]
    position = input_info[-1]
    year,month,day,start = input_info[:4]
    date = datetime.datetime(year,month,day,start,0,0)
    if not datas[(date,position)]:
        while True:
            name = input('请输入姓名与联系方式(李明144333)：')
            if name:
                datas[(date,position)] = name
                break
    else:
        reply = input('是否排队等待（y/n）:')
        if reply == 'y':
            while True:
                name = input('请输入姓名与联系方式(李明144333)：')
                if name:            
                    waiter.append((date,position,name))
                    break
        else:
            # 找出最近时间未预订的机位
            infos = [k for k,v in datas.items() if not v]
            info = [abs(k[0]-date) for k in infos] #时间作差
            latest = min(info)
            res = infos[info.index(latest)]
            print(res)
            while True:
                name = input('请输入姓名与联系方式(李明144333)：')
                if name:
                    datas[res] = name
                    break

def unreg(datas, waiter):
    input_info = input('请输入年月日、时间段开始点及机位号(2019,1,8,10,3):')
    input_info = [i for i in input_info.split(',')]
    if (not all([i.isdigit() for i in input_info])) or len(input_info) != 5:
        print('输入信息有误，请按格式输入：')
        return
    input_info = [int(i) for i in input_info]
    position = input_info[-1]
    year,month,day,start = input_info[:4]
    date = datetime.datetime(year,month,day,start,0,0)
    # 有等待者可以自动预订
    for w in waiter:
        if (date,position) == (w[0],w[1]):
            datas[(date,position)] = w[2]
            waiter.remove(w)
            break

def query_waiter(waiter):
    if waiter:
        wait = sorted(waiter,key = lambda w:w[0])
        for w in wait:
            print(w[2])
    else:
        print('无等待预订者！')

def main():
    datas = init()
    waiter = []
    while True:
        print('------------------------')
        print('机位信息－－q')
        print('机位预订－－r')
        print('取消预订－－u')
        print('查询等待－－w')
        print('退出系统－－exit')
        print('------------------------')
        command = input('请输入命令：')
        if command == 'q':
            query(datas)
        elif command == 'r':
            reg(datas, waiter)
        elif command == 'u':
            unreg(datas, waiter)
        elif command == 'w':
            query_waiter(waiter)
        elif command == 'exit':
            break
        else:
            print('请输入正确的命令！')

if __name__ == '__main__':
    main()
