#!/usr/bin/env python
# coding: utf-8

def parase_codes(codes):
    # 用列表推导法解析字符串
    return [char1 + char2 for char1,char2 in zip(codes[::2],codes[1::2])]

# 定义读取配置文件的函数
def get_config(configfile):
    # 建立空字典
    configDict = {}
    # 打开文件
    with open(configfile) as f:
        # 逐行处理
        for line in f:
            k, v = line.strip().split(':')
            configDict.setdefault(k, int(v))
    # 返回处理结果
    return configDict

# 定义处理一行奖金数
def get_prize(my_codes, prizes, prize_config):
    # 初始化奖金数为0
    sumprize = 0
    for code, prize in zip(my_codes, prizes):
        # 计算一个7的奖金
        if code == 'YQ':
            sumprize += prize_config[prize]
        # 计算二个7的奖金
        elif code == 'EQ':
            sumprize += prize_config[prize] * 2
        # 计算三个7的奖金
        elif code == 'SQ':
            sumprize += prize_config[prize] * 3
    # 奖金不为0时返回
    if sumprize:
        return str(sumprize) + '\n'
    # 奖金为0时返回
    else:
        return "中奖金额：0\n"

# 字义读取游戏数据文件并处理结果的函数
def get_data(configfile, filename):
    # 初始化存放结果的列表
    res = []
    # 调用函数，获取游戏配置
    prize_config = get_config(configfile)
    # 打开游戏数据文件并逐行处理
    with open(filename) as f:
        for line in f:
            # 分别取出号码和对应奖金代码
            my_codes, prizes = line.split()
            # 调用函数分割字符串
            my_codes = parase_codes(my_codes)
            # 调用函数获取奖金结果
            info = get_prize(my_codes, prizes, prize_config)
            # 保存一行正理结果
            res.append(info)
    # 返回结果
    return res

# 定义主函数
def main(configfile='GameDateconfig.txt', filename='GameData.txt'):
    # 调用函数获取奖金处理结果
    res = get_data(configfile, filename)
    # 打开文件写入处理结果
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(''.join(res))

main()
