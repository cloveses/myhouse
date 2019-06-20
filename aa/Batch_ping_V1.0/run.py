# -*- coding:UTF-8 -*-
#*********************************************##########################        #############
#------->>>>>>Author:秋某人的傻逼                    *#############     ###    ##     #########
#------->>>>>>Name:熊猫最爱皮卡丘                         *##########      ####     #########
#------->>>>>>Target:批量TCP-ping软件V1.0             *################           #########
#*********************************************############################    #########
#####################################################################################


# import subprocess
# import time

# pros = []
#     for m in list:
#         cmd = 'python %s %s'%('./Tcp_Batch_Ping.py',m)
#         # scanwish = os.system(cmd)
#         print(cmd)
#         pros.append(subprocess.Popen(cmd))
# for p in pros:
#     p.wait()

# cd /d d:\work\myhouse\aa\Batch_ping_V1.0

from multiprocessing import Pool, freeze_support
from Tcp_Batch_Ping import batch_ping_main

if __name__ == '__main__':
    
    freeze_support()

    lst = []
    for i in open('hosts.txt','r'):
        lst.append(i.strip())

    p = Pool(len(lst))
    for ip in lst:
        p.apply_async(batch_ping_main, args=(ip,))
    p.close()
    p.join()

