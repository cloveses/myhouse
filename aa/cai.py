#!/usr/bin/env python
# coding: utf-8

def strsplittolist(str1):
    list1 = list()                # 准备列表存储该函数的返回值
    i = 0                         # 初始化循环变量i，i表示str1字符串的索引，初始化为0
    while(i<len(str1)):           # 循环判断条件：当索引i的值小于str1字符串的长度，执行循环
        list1.append(str1[i:i+2]) # 循环体：每次循环在str1中取两个连续的字符，将其添加到列表中
        i = i + 2                 # 因为上条语句每次取两个字符，故循环变量每次增2
    return list1                  # 循环结束，返回list1

def CharprizeToNum(prizelist,configDict):
    prize = list()
    for x in prizelist:
        prize.append(configDict[x])
    return prize
        
def isWin(mynumlist,yournumlist,prizelist):
    sumprize = 0
    for x in yournumlist:          # 遍历中奖号码列表中的每一个元素
        for y in range(len(mynumlist)): # 遍历我的号码列表中的每个索引
            if x == mynumlist[y]:
                sumprize = sumprize + prizelist[y]
    return sumprize

# 准备配置文件全路径
path1 = r'D:\python.txt'
# 读配置文件GameDateconfig，将配置文件的内容保存到一个字典里configDict
configDict = {}  
# 读配置文件    
with open(path1,'r') as fp:               # 以只读方式打开一个文件
    for line in fp:                       # 一行一行的读配置文件，line就是配置文件中的一行
        list2 = line.strip().split(':')   # 删除每行字符串首尾的空格、\n和\t,并将每行字符串按照：拆分成列表
        configDict.setdefault(list2[0],int(list2[1])) 
print(configDict)

# 读取数据文件，解析数据行，提取我的号码列表、中奖号码列表和中奖金额列表            
# 准备数据文件全路径
path = r'D:\python1.txt' 

resultlist = list()               #  存储每条彩票数据的中奖信息 
with open(path,'r') as fp:        # 打开数据文件GameData，返回fp
    for line in fp: 
        strlist = line.split()    # 调用split函数，将strdata以空字符分解成列表，列表中有三个字符串元素
        print(strlist)
        # 调用strsplittolist函数，将我的号码字符串进行拆分，每两位为一个数字
        mylist = strsplittolist(strlist[0]) 
        # 调用strsplittolist函数，将你的号码字符串进行拆分，每两位为一个数字
        yourlist = strsplittolist(strlist[1]) 
        # 调用CharprizeToNum将金额字符转化为数字
        prizelist = CharprizeToNum(strlist[2],configDict)
        # 判断是否中奖
        prize = isWin(mylist,yourlist,prizelist)
        if prize == 0:
            strresult = "未中奖\n"
        else:
            strresult = "中奖，中奖金额是" + str(prize) + '\n'
        print(strresult)
        resultlist.append(strresult)
path2 = r'D:\python2.txt'
with open(path2,'w') as fp:
    for x in resultlist:
        fp.write(x)  