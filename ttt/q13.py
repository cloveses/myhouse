import queue
import datetime
import time, random

class Car:
    # 汽车编号
    code = -1

    def __init__(self):
        self.code = Car.code + 1
        Car.code += 1

    # 进入并初始化计时
    def enter(self):
        self.start = datetime.datetime.now()
        print('enter in:',self.code)

    # 退出计时并计费
    def exit(self):
        end = datetime.datetime.now()
        duratin = end - self.start
        minutes = duratin.seconds # / 60
        print("code:{} duratin:{} fee:{}".format(self.code,minutes,minutes * 0.1))
        return minutes * 0.1


class Station:

    def __init__(self, capacity):
        self.datas = queue.LifoQueue(capacity)
        self.temp = queue.Queue()
        self.total_fee = 0

    # 有车辆请求进场，满则排队，否则进场
    def request(self, car):
        if self.datas.full():
            print('Wait:', car.code)
            self.temp.put(car)
        else:
            car.enter()
            self.datas.put(car)

    # 有车辆请求离开
    def out(self, car):
        outs = []
        while True:
            c = self.datas.get()
            if c == car:
                self.total_fee += c.exit()
                for out in outs:
                    self.datas.put(out)
                # 便道等待车进入
                if not self.temp.empty():
                    wait_c = self.temp.get()
                    wait_c.enter()
                    self.datas.put(wait_c)
                break
            else:
                outs.append(c)
                print('out temp:', c.code)

if __name__ == '__main__':
    cars = [Car() for i in range(12)]
    s = Station(5)
    for c in cars[:6]:
        s.request(c)
        time.sleep(random.randint(2,6))
    s.out(cars[2])
    time.sleep(random.randint(2,4))
    s.out(cars[4])

    print(s.total_fee)
