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
        ds = os.path.splitext(file)
        # print(data)
        data = binascii.unhexlify(data)
        # print(data)
        f = open(''.join((ds[0],'_err',ds[-1])), 'wb')
        f.write(data)
        f.close()

if __name__ == '__main__':
    edit('test')