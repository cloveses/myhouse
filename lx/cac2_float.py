
# 计算一个数的规格化浮点数并输出

def main():
    while True:
        number = input('请输入要转换的数：')
        if number.strip().replace('.','').replace('-','').isdigit():
            number = float(number)
            break
        else:
            print('输入不符合要求！')

    if number == 0:
        print('0_0000000_0_000000000000000')
        return

    if number > 0:
        sign_tail = '0'
    else:
        sign_tail = '1'

    number = abs(number)
    integer = int(number)
    integer = bin(integer)[2:]
    if integer == '0':
        exponent = 0
    else:
        exponent = len(integer)

    fraction =  number - int(number)
    if fraction == 0:
        fraction_str = '0000000000000000'
    else:
        fraction_lst = []
        while True:
            fraction *= 2
            fraction_int = int(fraction)
            fraction_lst.append(str(fraction_int))
            fraction = fraction - fraction_int
            if '1' in fraction_lst and len(fraction_lst[fraction_lst.index('1'):]) >= 16:
                break
        fraction_str = ''.join(fraction_lst)

    if exponent == 0:
        i = 0
        while not fraction_str[i] == '1':
            exponent -= 1
            i += 1
        fraction_str = fraction_str[i:]
        exponent = bin(256 + exponent)
        print('_'.join((exponent[-8],exponent[-7:],sign_tail,fraction_str)))
    else:
        exponent = bin(256 + exponent)
        fraction_str = integer + fraction_str
        print('_'.join((exponent[-8],exponent[-7:],sign_tail,fraction_str)))


if __name__ == '__main__':
    main()
