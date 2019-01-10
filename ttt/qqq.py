

def action(m=3,start=1):
    if m <= 1:
        print('人数必须大于1！')
    inits = [True,] * m
    for k in range(m):
        datas = inits[:]
        start = 1
        i = k
        flag = False
        while True:
            # 成功则退出
            if datas[0] and not any(datas[1:]):
                print(k)
                flag = True
                break

            # 失败退出
            if start % 5 == 0 and i == 0 and any(datas[1:]):
                break

            # print((i,start),end=';')
            i += 1
            if i >= len(datas):
                i = 0
            if datas[i]:
                start += 1
                if start % 5 == 0:
                    datas[i] = False

        # print(datas)
        if flag:
            break

# 士兵节点
class Soldier:
    _seq = 0
    def __init__(self, post='soldier'):
        self.post = post
        self.pre = self
        self.next = self
        self.seq = Soldier._seq
        Soldier._seq += 1

    def set_next(self, soldier):
        self.next = soldier

    def set_pre(self,soldier):
        self.pre = soldier

    def display(self):
        print((self.post,self.seq),end=' ')

    def init_seq(self):
        Soldier._seq = 0


# 创建循环链
def create_nodes(m=3):
    post = Soldier(post='leader')
    soldiers = [post,]
    for i in range(m-1):
        soldiers.append(Soldier())
    for i,soldier in enumerate(soldiers):
        soldier.set_next(soldiers[i+1 if i+1 <len(soldiers) else 0])
        soldier.set_pre(soldiers[i-1])
    return post

def display(node):
    start = node.seq
    # print(start)
    current = node
    while True:
        current.display()
        current = current.next
        if current.seq == start:
            break
    print()
    # print(current.seq)

def get_result(m=3):
    # 遍历尝试
    for i in range(m):
        node = create_nodes(m)
        node.init_seq()
        k = i
        # 获取尝试的起始节点
        flag = False
        while True:
            if node.seq == i:
                break
            else:
                node = node.next
        # 开始尝试
        count = 1
        while True:

            print((count,node.seq),end =' ')
            display(node)

            # 成功退出
            if node.next == node and node.pre == node and node.post == 'leader':
                print(i)
                flag = True
                break

            # 失败退出
            if count % 5 == 0 and node.post == 'leader':
                break
            # 对遍历的节点处理
            if count % 5 == 0:
                node.pre.set_next(node.next)
                node.next.set_pre(node.pre)
                # temp = node
            node = node.next
            count += 1

        print()

        if flag:
            break

if __name__ == '__main__':
    # action(2)
    # get_result(2)
    # action(3)
    get_result(3)
    # action(4)
    get_result(4)
    # action(5)
    # get_result(5)
    # action(6)
    # get_result(6)
    # action(7)
    # get_result(7)
    # action(10)
