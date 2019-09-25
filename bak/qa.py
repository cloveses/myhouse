    
class MyQueue:
    
    def __init__(self):
        # 持有队列首个元素
        self.data = []

    def Enqueue(self, d):
        self.data.append(d)

    def PrintQueue(self):
        # 队列不为空则循环打印队列中数据
        if self.data:
            for d in self.data:
                print(d, end='')
            print()
        else:
            print('Empty!')
        
    def Dequeue(self):
        # 队列为空则无法出列
        if not self.data:
            print('Queue is empty!')
        else:
            # 队列不为空，则取出首个元素，将当前队列首个元素置为下一个
            d = self.data[0]
            self.data = self.data[1:]
            return d

    def Count(self):
        return len(self.data)

    def Contains(self, d):
        if d in self.data:
            return True
        else:
            return False

q = MyQueue()
q.Enqueue(1)
q.PrintQueue()

q.Enqueue(2)
q.PrintQueue()

for i in range(3,8):
    q.Enqueue(i)
q.PrintQueue()

for i in range(4):
    print(q.Dequeue())
    q.PrintQueue()

for i in range(5,9):
    print(i,q.Contains(i))
print(q.Count())