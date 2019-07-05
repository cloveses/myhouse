#!/usr/bin/env python
# coding: utf-8

def parase_codes(codes):
    return [char1 + char2 for char1,char2 in zip(codes[::2],codes[1::2])]

def get_config(filename):
    configDict = {}
    with open(filename) as f:
        for line in f:
            k, v = line.strip().split(':')
            configDict.setdefault(k, int(v))
    return configDict

def get_prize_data(my_codes, prize_codes, prizes, prize_config):
    code_prize = {}
    for prize_code,prize in zip(prize_codes, prizes):
        code_prize[prize_code] = prize_config[prize]
    sumprize = 0
    for my_code in my_codes:
        if my_code in code_prize:
            sumprize += code_prize[my_code]
    if sumprize:
        return "中奖，中奖金额是" + str(sumprize) + '\n'
    else:
        return "未中奖\n"

def get_data(configfile, filename):
    res = []
    prize_config = get_config(configfile)
    with open(filename) as f:
        for line in f:
            my_codes, prize_codes, prizes = line.split()
            my_codes = parase_codes(my_codes)
            prize_codes = parase_codes(prize_codes)
            info = get_prize_data(my_codes, prize_codes, prizes, prize_config)
            res.append(info)
    return res

def main(configfile='GameDateconfig.txt', filename='GameData.txt'):
    res = get_data(configfile, filename)
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(''.join(res))

if __name__ == '__main__':
    main()
