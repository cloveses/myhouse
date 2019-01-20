# coding: utf-8

import paramiko
import re
import os
from time import sleep

# 定义一个类，表示一台远端linux主机
# 参考https://www.cnblogs.com/haigege/p/5517422.html wyc
class Linux(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=3000):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 2

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print (u'连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print (self.chan.recv(65535).decode('utf-8'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception as e1:
                if self.try_times != 0:
                    print (u'连接%s失败，进行重试' %self.ip)
                    self.try_times -= 1
                else:
                    print (u'重试2次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()



    # 发送要执行的命令
    def send(self, cmd):
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        p = re.compile(r':~ #')
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        print (u'-----命令已执行-----')
        while True:
            sleep(1)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            print((ret) )

    # ------获取本地指定目录及其子目录下的所有文件------
    def __get_all_files_in_local_dir(self, local_dir):
        # 保存所有文件的列表
        all_files = list()

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = os.listdir(local_dir)
        for x in files:
            # local_dir目录中每一个文件或目录的完整路径
            filename = os.path.join(local_dir, x)
            # 如果是目录，则递归处理该目录
            if os.path.isdir(x):
                all_files.extend(self.__get_all_files_in_local_dir(filename))
            else:
                all_files.append(filename)
        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        t = paramiko.Transport(sock=(self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # 去掉路径字符穿最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取本地指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_in_local_dir(local_dir)
        # 依次put每一个文件
        for x in all_files:
            filename = os.path.split(x)[-1]
            remote_filename = remote_dir + '/' + filename
            print (x)
            print (remote_filename)
            print (u'Put文件%s传输到%s中...' % (filename,self.ip))
            sftp.put(x, remote_filename)



if __name__ == '__main__':
    host = Linux('172.17.126.34', 'wfgch', 'wangj123')
    host.connect()
    host.send('amos wf1212')
    host.send('lt all')
    host.send('alt')

    #remote_path = r'/home/wfgch/GML1'
    #local_path = r'D:\干掉后台开站的\SSH上传下载文件\test'
    #host.sftp_put_dir('D:/干掉后台开站的/SSH上传下载文件/test.mo, /home/wfgch/GML1\test.mo')
    #hostArray=['172.17.126.34','wfgch','wangj123']
    #for x in hostArray:
      #host = Linux(x[0], x[1], x[2])
      #host.sftp_put_dir(local_path, remote_path)
    host.close()