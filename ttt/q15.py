# [[date,duration,False],...]

import datetime

def init():
    datas = {}
    td = datetime.date.today()
    for i in range(7):
        for j in range(6):
            for k in range(1,21):
                datas[(datetime.datetime(td.year, td.month, td.day,8 + j * 2,0,0) + datetime.timedelta(days=i),k)] = False

    print(datas)
    return datas

def query(datas):
    input_info = input('请输入年月日、时间段开始点及机位号(2019,1,8,10,3):')
    input_info = [i for i in input_info.split(',')]
    if (not all([i.isdigit() for i in input_info])) or len(input_info) != 5:
        print('输入信息有误，请按格式输入：')
        return
    input_info = [int(i) for i in input_info]
    position = input_info[-1]
    year,month,day,start = input_info[:4]
    date = datetime.datetime(year,month,day,start,0,0)
    if datas[(date,position)]:
        print(date,'已占用！')
    else:
        print(date,'未占用！')

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
        reply = input('是否排除等待（y/n）:')
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
    for w in waiter:
        if (date,position) == (w[0],w[1]):
            datas[(date,position)] = w[2]
            waiter.remove(w)
            break

def query_waiter(waiter):
    wait = sort(waiter,key = lambda w:w[0])
    for w in wait:
        print(w[2])






if __name__ == '__main__':
    # main()
    init()
