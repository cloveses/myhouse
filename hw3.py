def main():
    datas = []
    while True:
        s = input('请输入一个数值:')
        if s == 'done':
            break
        try:
            n = float(s)
        except:
            print('你输入的"%s"不是数值！' % s)
        else:
            datas.append(n)
    print('----------------')
    print('平均数：',sum(datas)/len(datas))
    print('最大值：',max(datas))
    print('最小值：',min(datas))

if __name__ == '__main__':
    main()
