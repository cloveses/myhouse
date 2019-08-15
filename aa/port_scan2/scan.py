# -*- coding:UTF-8 -*-
#*********************************************
#------->>>>>>Author:秋某人的傻逼                    *
#------->>>>>>Name:熊猫最爱皮卡丘                        *
#------->>>>>>Target:端口实时监控工具V4.0代码重构版本  *
#*********************************************
import os
import socket
import datetime
import telnetlib
#端口扫描主程序
#TCP扫描，syn模块
def mkdir(path):
    now = datetime.datetime.now()
    # 去除首位空格
    # path = path.strip()
    # 去除尾部 \ 符号
    # path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False
#------------------------------------------------

def syn_portscan(ip,port):
    timeout = 0.05
    socket.setdefaulttimeout(timeout)  # 这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, port))
        print('INFO | IP {0} PORT {1} is open'.format(ip, str(port)))
        now = datetime.datetime.now()
        path = 'portscan_results/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '/synscan'
        mkdir(path)
        with open(path + '/results.txt', 'a+') as f:
            ip_port = ip + '_' + str(port)
            f.write(ip_port)
            f.write('\n')
            f.close()
    except Exception as e:
        print(('INFO | IP {0} PORT {1} is close'.format(ip, str(port))), '|', '失败原因：', e)
    finally:
        server.close()
#telnet扫描模块
def telnet_portscan(ip,port):
    try:
        tel = telnetlib.Telnet(ip, port, timeout=0.05)
        print(tel)
        print('INFO | IP {0} PORT {1} is open'.format(ip, str(port)))
        now = datetime.datetime.now()
        path = 'portscan_results/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '/telnetscan'
        mkdir(path)
        with open(path + '/results.txt', 'a+') as f:
            ip_port = ip + '_' + str(port)
            f.write(ip_port)
            f.write('\n')
            f.close()
    except Exception as e:
        print(('INFO | IP {0} PORT {1} is close'.format(ip, str(port))), '|', '失败原因：', e)