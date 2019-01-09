
#### err

def action(m=3,start=1):
    inits = [True,] * m
    for i in range(m):
        datas = inits[:]
        start = 1
        k = i
        while True:
            k += 1
            if k == 0 and 


if __name__ == '__main__':
    # for i in range(3,4):
    #     print(i,end=' ')
    #     action(i)
    # action(2)
    # action(3)
    # action(4)
    action(5)
