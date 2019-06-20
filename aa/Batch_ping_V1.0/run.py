# -*- coding:UTF-8 -*-
#*********************************************##########################        #############
#------->>>>>>Author:秋某人的傻逼                    *#############     ###    ##     #########
#------->>>>>>Name:熊猫最爱皮卡丘                         *##########      ####     #########
#------->>>>>>Target:批量TCP-ping软件V1.0             *################           #########
#*********************************************############################    #########
#####################################################################################


import subprocess
import time

list = []
for i in open('hosts.txt','r'):
    list.append(i.strip())
    for m in list:
        cmd = 'python %s %s'%('./Tcp_Batch_Ping.py',m)
        # scanwish = os.system(cmd)
        print(cmd)
        process = subprocess.Popen(cmd)
        process.wait()