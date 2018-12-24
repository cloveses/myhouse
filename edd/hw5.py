class program:
    def __init__(self, s):
        self.progs = s
        self.vars = {}
        self.blocks = {}
        self.graphs = {}

    def parse(self, st):
        list = []
        for prog in st:
            if ':' in prog:
                label = prog[:prog.index(':')]
                if 'if' in prog:
                    list.append(label)
                    list.append('if')

                elif 'while' in prog:
                    list.append(label)
                    list.append('while')

                else:
                    list.append(label)

            elif 'fi' in prog:
                list.append('fi')

            elif 'done' in prog:
                list.append('done')

        block = []
        block.append(list[0])
        get = False
        for i in list[1:]:
            if i == 'if':
                a = 0
                a = list.index('if', a)
                a = a + 1
                block.append('if')
                block.append(list[a])

            elif i == 'fi':
                b = 0
                b = list.index('fi', a)
                b = b + 1
                block.append(list[b])

            elif i == 'done':
                c = 0
                c = list.index('done', c)
                c = c + 1
                block.append(list[c])

            elif i == 'while':
                d = 0
                d = list.index('while', d)
                block.append(list[d - 1])
                d = d + 1
                block.append('while')
                block.append(list[d])

            else:
                pass
        block.append('finish')
        block.insert(0,'begin')

        graph = []
        for i in block[:]:
            if i == 'if':
                pass
            elif i == 'fi':
                pass
            elif i == 'while':
                pass
            elif i == 'done':
                pass
            else:
                graph.append(i)
        new_graph = []
        graph.remove('finish')
        graph.remove('begin')
        key = sorted(graph)
        lenth = len(key)
        print('[', end='')
        for i in key[:]:
            for j in key[:]:
                a = block.index(i)
                b = block.index(j)
                if block[a + 1] == 'if':
                    if a + 2 == b:
                        print('1', end='')
                    elif a + 3 == b:
                        print('1', end='')
                    else:
                        print('0', end='')
                elif block[a - 1] == 'if':
                    if a + 1 == b:
                        print('1', end='')
                    else:
                        print('0', end='')
                elif block[a + 1] == 'while':
                    if a + 2 == b:
                        print('1', end='')
                    elif a + 3 == b:
                        print('1', end='')
                    else:
                        print('0', end='')
                elif block[a - 1] == 'while':
                    if a - 2 == b:
                        print('1', end='')
                    else:
                        print('0', end='')
                else:
                    if a + 1 == b:
                        print('1', end='')
                    else:
                        print('0', end='')

                if key.index(j) == lenth - 1:
                    if key.index(i) == lenth-1:
                        print(']')
                    else:
                        print(';',end='')
                else:
                    print(',',end='')
                    


    def getCFG(self):
        
        self.parse(s)

def orders():
    n = 0
    s = []
    while True:
        n += 1
        order = input().strip()
        s.append(order)
        if "}" in order: break
    return s

s = orders()
p = program(s)
p.getCFG()












                    





                
