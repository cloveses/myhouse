import os
import binascii

def get_files(directory):
    files = []
    files = os.listdir(directory)
    files = [f for f in files]
    files = [os.path.join(directory,f) for f in files]
    return files

def edit(directory):
    pos = input('输入修改位置：')
    val = input('输入修改成的值：')
    length = len(val)
    start = int(pos, 16) * 2
    # print(start)
    val = binascii.hexlify(bytes((int(''.join((i,j)), 16) for i,j in zip(val[::2],val[1::2]))))
    # print(val)
    files = get_files(directory)
    for file in files:
        f = open(file, 'rb')
        data = binascii.hexlify(f.read())
        f.close()
        # print(data)
        # print(data[:start])
        data = data[:start] + val + data[start+length:]
        # ds = os.path.splitext(file)
        # print(data)
        data = binascii.unhexlify(data)
        # print(data)
        # f = open(''.join((ds[0],'_err',ds[-1])), 'wb')
        f = open(file, 'wb')
        f.write(data)
        f.close()

def cacu(directory):
    pos = input('输入起止位置(eg: 1c-1f),不输入表示全部 ：')
    if pos:
        start, end  = [int(p, 16) for p in pos.split('-')]
    val = input('输入参与计算的值：')
    val = int(val, 16)
    opr = input('选择计算方法(1 默认为加法,2 为异或)：')
    if not opr:
        opr = '1'

    files = get_files(directory)
    for file in files:
        f = open(file, 'rb')
        datas = bytearray(f.read())
        f.close()
        if not pos:
            start, end = 0, len(datas) - 1
        for i in range(start, end+1):
            if opr == '1':
                datas[i] = (datas[i] + val) % 256
            elif opr == '2':
                datas[i] ^= val
        # with open('res.txt', 'wb') as f:
        #     f.write(datas)
        with open(file, 'wb') as f:
            f.write(datas)

if __name__ == '__main__':
    # edit('test')
    cacu('test')