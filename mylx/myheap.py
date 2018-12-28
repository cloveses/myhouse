

class Heap:
"""
用树来表示堆
堆的每个节点都小于其左右子节点
用数组来表示堆，父节点的序号（开始值为1）为子节点序号/2（取整数）
堆的最小值总是根结点
"""
    def __init__(self, datas=None):
        if datas:
            self.datas = datas
        else:
            self.datas = []

    def insert(self, n):
        self.datas.append(n)
        # 堆中元素为1，不用变化
        if len(self.datas) == 1:
            return
        seq = len(self.datas)
        while True:
            # 到达根节点
            if seq // 2 - 1 < 0:
                break
            # 比较父节点与新节点并更新节点值
            if self.datas[seq // 2 - 1] > n:
                self.datas[seq - 1] = self.datas[seq // 2 -1]
                self.datas[seq // 2 -1] = n
            else:
                break
            # 更新处理节点
            seq = seq // 2
        print(self.datas)

if __name__ == '__main__':
    heap = Heap()
    heap.insert(13)
    heap.insert(9)
    heap.insert(15)
    heap.insert(3)
    heap.insert(7)
    heap.insert(2)