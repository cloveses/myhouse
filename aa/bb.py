# 数据转换为真假列表
def get_bool_list(x):
    ret = []
    sign = False if x >= 0 else True
    x = abs(x)
    int_part = int(x)
    bin_int_part = bin(int_part)[2:]
    bin_bool_list = [True if d == '1' else False for d in bin_int_part]
    if len(bin_bool_list) < 20:
        bin_bool_list = [False, ] * (20-len(bin_bool_list)) + bin_bool_list
    elif len(bin_bool_list) > 20:
        return 'out range!'
    other_part = x - int_part
    other_bool_list = []
    for i in range(20):
        other_part = other_part * 2
        if int(other_part) == 0:
            other_bool_list.append(False)
        else:
            other_bool_list.append(True)
            other_part -= 1
    ret.append(sign)
    ret.extend(bin_bool_list)
    ret.extend(other_bool_list)
    return ret

# 求补码
def get_encode(number_lst):
    if not number_lst[0]:
        return number_lst
    if True not in number_lst[1:]:
        return [False,] * 41

    for i,d in enumerate(number_lst[::-1], 1):
        if d:
            break
    for j in range(1,len(number_lst) - i):
        number_lst[j] = not number_lst[j]
    return number_lst

#全加器
def FA(a, b, c):
    Carry = (a and b) or (b and c) or (a and c)
    Sum = (a and b and c) or (a and (not b) and (not c))\
        or ((not a) and b and (not c)) or ((not a) and (not b) and c)
    return Carry, Sum

#用真假值列表求和
def add(x, y):
    L = []
    Carry = False
    for i in range(len(x)-1, -1, -1):
        Carry,Sum = FA(x[i], y[i], Carry)
        L = [Sum] + L
    return(Carry, L)

#真假值列表转实数
def get_real(L):
    if L[0]:
        L = get_encode(L)
    int_part = int(''.join(['1' if d else '0' for d in L[1:21]]), 2)
    for i,d in enumerate(L[21:], 1):
        if d:
            int_part += 1 / (2 ** i)
    if L[0]:
        int_part = -int_part
    return int_part


def main(x=13.625, y=-12.125):
    xb = get_encode(get_bool_list(x))
    yb = get_encode(get_bool_list(y))
    c, L = add(xb, yb)
    # print(c, L)
    print(x, '+ (', y, ') =', get_real(L))
if __name__ == '__main__':
    main()
    main(100.4125, -34.5)