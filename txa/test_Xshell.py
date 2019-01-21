#!/usr/bin/env python
#coding:utf8
import paramiko
#创建sshclient对象
ssh = paramiko.SSHClient()
#允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#调用connect方法连接服务器
ssh.connect(hostname='172.17.126.34',port=22,username='wfgch',password='wangj123')
while True:
    input_command = input('>>>:')
    if input_command == 'quit':
        break
    #执行命令，输出结果在stdout中，如果是错误则放在stderr中
    stdin,stdout,stderr = ssh.exec_command(input_command)

    result = stdout.read() #read方法读取输出结果
    if len(result) == 0:  #判断如果输出结果长度等于0表示为错误输出
        print(stderr.read())
    else:
        print(str(result,'utf-8'))
ssh.close()




