# -*- coding:UTF-8 -*-
# import os
# ip = '127.0.0.1'
# cmd2 = 'ping %s -n 100' % (ip)
# pingIp = os.system(cmd2)  # 执行100次ping命令
# print(pingIp)

import re
pingIp = '''正在 Ping 94.191.18.96 具有 32 字节的数据:
来自 94.191.18.96 的回复: 字节=32 时间=68ms TTL=114
来自 94.191.18.96 的回复: 字节=32 时间=63ms TTL=114
94.191.18.96 的 Ping 统计信息:
    数据包: 已发送 = 2，已接收 = 2，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 63ms，最长 = 68ms，平均 = 65ms'''
print(type(pingIp))
pingIp2 = re.compile(r'来自..+', re.M).findall(str(pingIp))  # 通过正则表达式筛选出需要的哪一行
print(pingIp2)