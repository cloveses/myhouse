    # 用于存储数据的节点类
    class Node:
        def __init__(self, data, npointer=None):
            # 数据
            self.data = data
            # 指向下一条数据
            self.npointer = npointer
            
        # 获取下一条数据
        def get_next(self):
            return self.npointer
        
        # 设定下一条数据
        def set_next(self, node):
            self.npointer = node
        
        # 获取节点的数据
        def get_data(self):
            return self.data

class MyQueue:
    
    def __init__(self,first_node=None):
        # 持有队列首个元素
        self.first_node = first_node
        # 存储队列中元素个数
        self.__count = 0

    def Enqueue(self, data):
        # 队列不为空则找到最后一个元素后，在其后增加一个节点类
        if self.first_node:
            np = self.first_node
            for i in range(self.__count - 1):
                np = np.get_next()
            np.set_next(Node(data))
        # 队列为空，直接创建节点类并置为首个节点
        else:
            self.first_node = Node(data)
        self.__count += 1

    def PrintQueue(self):
        # 队列不为空则循环打印队列中数据
        if self.first_node:
            np = self.first_node
            while True:
                if np:
                    print(np.get_data(), end=' ')
                    np = np.get_next()
                else:
                    break
            print()
        else:
            print('Empty!')
        
    def Dequeue(self):
        # 队列为空则无法出列
        if not self.first_node:
            print('Queue is empty!')
        else:
            # 队列不为空，则取出首个元素，将当前队列首个元素置为下一个
            d = self.first_node.get_data()
            self.first_node = self.first_node.get_next()
            self.__count -= 1
            return d

    def Count(self):
        return self.__count

    def Contains(self, data):
        if not self.first_node:
            print('Not find!')
            return False
        else:
            # 队列不为空启遍历队列，查询要找的值
            np = self.first_node
            while np:
                if np.get_data() == data:
                    print('Find!')
                    return True
                else:
                    np = np.get_next()
            print('Not find!')
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
