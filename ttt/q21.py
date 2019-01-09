
#### err

def action(m=3,start=1):
    inits = list(range(m))
    for i in range(m):
        datas = inits[:]

        while len(datas) > 1:
            pre = 0
            segments,remain = divmod(len(datas), 5)
            seqs = [i*5-1-pre for i in range(segments)]
            rdata = [datas[s] for s in seqs]
            if all(rdata):
                for s in seqs:
                    del datas[s]
            else:
                break
            pre = remain
        else:
            print(i)
            break

if __name__ == '__main__':
    # for i in range(3,4):
    #     print(i,end=' ')
    #     action(i)
    # action(3)
    # action(4)
    action(5)
