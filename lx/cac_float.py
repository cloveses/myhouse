# 计算一个数的规格化浮点数并输出，阶码为补码，尾数为原码

def deal_tail(tail):
    if tail == 0:
        return '0000000000000000'
    s = ''
    while True:
        tail *= 2
        integer_part = int(tail)
        s += str(integer_part)
        tail -= integer_part
        if '1' in s and len(s[s.index('1'):]) >= 16:
            return s


def main():
    while True:
        try:
            num = float(input('请输入一个浮点数：'))
            break
        except:
            print('你输入的不是浮点数！')
    if num == 0:
        print('0_0000000_0_000000000000000')
        return
    if num > 0:
        tail_sign = '0'
    else:
        tail_sign = '1'

    num = abs(num)
    int_part = int(num)
    int_part = bin(int_part)[2:]
    if int_part == '0':
        jie = 0
    else:
        jie = len(int_part)

    tail_str = deal_tail(num - int(num))
    if jie == 0:
        i = 0
        while not tail_str[i] == '1':
            jie -= 1
            i += 1
        tail_str = tail_str[i:]
        jie = bin(256 + jie)
        print('_'.join((jie[-8],jie[-7:],tail_sign,tail_str)))
    else:
        jie = bin(256 + jie)
        tail_str = int_part + tail_str
        print('_'.join((jie[-8],jie[-7:],tail_sign,tail_str)))


if __name__ == '__main__':
    main()
