# flights [(code,starttime,endtime,src,dest,price,discount,max_people)]
# flights_info [(code,date,isfull,ordered)]
# customs[(name,idcode,num,code)]

import pickle
import datetime
import os

class Flight:

    def __init__(self, code, starttime, endtime, src, dest, price, discount, max_people, ordered=0):
        self.code = code
        self.starttime = starttime
        self.endtime = endtime
        self.src = src
        self.dest = dest
        self.price = price
        self.discount = discount
        self.max_people = max_people
        self.ordered = ordered

    def display(self):
        print('航班号：', self.code)
        print('起飞时间：', self.endtime)
        print('抵达城市：', self.dest)
        print('票价：', self.price)
        if self.max_people == self.ordered:
            print('满仓！')

    def has_seat(self):
        return self.max_people - self.ordered

class Order:
    _orderid = 0
    def __init__(self, orderid, code, idcode, num, name):
        self.orderid = orderid
        self.code = code
        self.idcode = idcode
        self.num = num
        self.name = name

def input_flights(flights):
    while True:
        params = {}
        params['code'] = input('code:')
        params['starttime'] = input('starttime(8:00):')
        params['endtime'] = input('endtime(9:00):')
        params['src'] = input('src:')
        params['dest'] = input('dest:')
        params['price'] = float(input('price:'))
        params['discount'] = float(input('discount(95折即：95：)')) / 100
        params['max_people'] = int(input('乘客数：'))
        if not all(params.values()):
            print('数据项不能为空：')
            continue
        params['starttime'] = datetime.time(*(map(int,params['starttime'].strip().split(':'))))
        params['endtime'] = datetime.time(*(map(int,params['endtime'].strip().split(':'))))
        flights.append(Flight(**params))
        yes = input('是否继续(n退出,其余继续)：')
        if yes == 'n':
            break

def edit_flights(flights):
    #将航班列表变成以航班号为键的字典
    dflights = {f.code:f for f in flights}
    print('目前所有航班：\n')
    print(list(dflights.keys()))
    while True:
        code = input('请输入修改航班号：')
        if not code:
            print('你的输入为空！')
        else:
            break
    if code in dflights:
        print('请输入修改的项目：')
        print('code, starttime, endtime, src, dest, price, discount, max_people')
        key = input()
        data = input('请输入数据：')
        if key in ('starttime','endtime'):
            setattr(dflights[code], key, datetime.time(*(map(int,data.strip().split(':')))))
        elif key == 'price':
            setattr(dflights[code], key, float(data))
        elif key == 'discount':
            setattr(dflights[code], key, float(data) / 100)
        elif key == 'max_people':
            setattr(dflights[code], key, int(data))
        else:
            setattr(dflights[code], key, data)
    return list(dflights.values())


def query(flights):
    #将航班列表变成以航班号为键的字典
    dflights = {f.code:f for f in flights}
    print(list(dflights.keys()))
    while True:
        code = input('请输入查询航班号：')
        if not code:
            print('你的输入为空！')
        else:
            break
    if code in dflights:
        dflights[code].display()
    else:
        print('无此航班！')

def query_dest(flights):
    while True:
        dest = input('请输入查询航班号：')
        if not dest:
            print('你的输入为空！')
        else:
            break
    for f in flights:
        if f.dest == dest:
            f.display()

def order(flights,orders):
    codes = {f.code:f.has_seat() for f in flights if f.has_seat()}
    print('可预订航班：')
    for code,seats in codes.items():
        print('航班号{} 座位数{}'.format(code,seats))
    print()
    while True:
        code = input('请输入预订航班号：')
        if not code:
            print('你的输入为空！')
        elif code not in codes:
            print('无此航班！')
        else:
            break
    while True:
        num = input('预订座位数：')
        if num and num.isdigit():
            num = int(num)
            if num > codes[code]:
                print('预订座位数太大！')
            else:
                while True:
                    name = input('你的姓名：')
                    idcode = input('你的证件号：')
                    if name and idcode:
                        orderid = Order._orderid + 1
                        print('-----------')
                        print('你的订单号',orderid)
                        print('-----------')
                        Order._orderid += 1
                        orders.append(Order(orderid=orderid, code=code, num=num, idcode=idcode, name=name))
                        for f in flights:
                            if f.code == code:
                                f.ordered += num
                                return

def cancel(flights, orders):
    while True:
        orderid = input('你的订单号：')
        if orderid and orderid.isdigit():
            orderid = int(orderid)
            break

    myorder = None
    for order in orders:
        if order.orderid == orderid:
            myorder = order
            break
    if not myorder:
        print('要取消的订单号不存在！')
        return
    orders.remove(myorder)
    for f in flights:
        if f.code == myorder.code:
            f.ordered -= myorder.num
            return
def main():
    flights = []
    orders = []
    if os.path.exists('flights.db'):
        with open('flights.db','rb') as f:
            flights = pickle.load(f)
    if os.path.exists('orders.db'):
        with open('orders.db','rb') as f:
            orders = pickle.load(f)
    print('-----------------')
    print('欢迎使用航班系统')
    print('输入航班信息－－i, 查询航班信息－－q, 按目的地查询－－a, 修改航班信息－－e')
    print('预订航班－－b, 退订航班－－c','退出系统－－exit')
    while True:
        command = input('请输入要执行的操作命令：')
        if command == 'i':
            input_flights(flights)
        elif command == 'q':
            query(flights)
        elif command == 'e':
            edit_flights(flights)
        elif command == 'b':
            order(flights, orders)
        elif command == 'c':
            cancel(flights,orders)
        elif command == 'a':
            query_dest(flights)
        elif command == 'exit':
            break
    with open('flights.db','wb') as f:
        pickle.dump(flights, f)
    with open('orders.db','wb') as f :
        pickle.dump(orders, f)

if __name__ == '__main__':
    main()
