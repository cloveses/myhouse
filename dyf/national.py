import os, functools, sys

def get_files(directory):
    files = []
    files = os.listdir(directory)
    files = [f for f in files]
    files = [os.path.join(directory,f) for f in files]
    return files

def deal(file, datas, deal_fun):
    contents = None
    with open(file, 'rb') as f:
        contents = f.read()
    if contents:
        contents = bytearray(contents)
    times = len(contents) // len(datas)
    for time in range(times):
        for i,data in enumerate(datas):
            pos = time * len(datas) + i
            contents[pos] = deal_fun(contents[pos], data)

    # return contents
    with open('res.txt', 'wb') as f:
        f.write(contents)

def deal_fun(a,b,opt):
    if opt == 0:
        s = a + b
    elif opt == 1:
        s = a - b
    elif opt == 2:
        s = a ^ b
    if s < 0 or s > 255:
        return 0
    else:
        return s

def main():
    opt = input('选择计算方法(0 默认为加法, 1 为减法 ,2 为异或)：')
    if opt not in ('0', '1', '2'):
        print('请输入正确的计算方式数码！')
        sys.exit(0)
    opt = int(opt)
    op_datas = input('输入参与计算的值(总长偶数位16进制数值串)：')
    if not op_datas:
        print('输入不能为空！')
        sys.exit(1)
    datas = []
    try:
        for p,n in zip(op_datas[0::2], op_datas[1::2]):
            datas.append(int(''.join((p,n)), 16))
    except:
        print('输入的16进制数值串有误！')
        sys.exit(0)
    df = functools.partial(deal_fun,opt=opt)
    for file in get_files('test'):
        deal(file, datas, df)

if __name__ == '__main__':
    main()