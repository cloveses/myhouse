import datetime
import configparser
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import http.client
import time
import sys
import paramiko
import re
import os
from time import sleep
import itchat
from itchat.content import *
import xlrd

def get_data(filename='告警对照表.xlsx', start=1):
     #既可以打开xls类型的文件，也可以打开xlsx类型的文件
    datas = []
    w = xlrd.open_workbook(filename)
    ws = w.sheets()[0]
    nrows = ws.nrows
    for i in range(start, nrows):
        data = ws.row_values(i)
        datas.append(data)
    #    print(datas)
    datas = {r[0]:r[1] for r in datas}
    return datas

warnnings = get_data()

def get_warnnings(infos, flag='Nr of active alarms are:'):
    all_warnnings = []
    if flag in infos:
        infos = infos.split('\n')[::-1][1:]
        for info in infos:
            if '=======' in info:
                break
            for k,v in warnnings.items():
                if k in info:
                    all_warnnings.append(v)
    if all_warnnings:
        return '\n'.join(all_warnnings[::-1])


#模拟Xshell功能
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
        self.try_times = 3

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
                    print (u'重试3次失败，结束程序')
                    print (u'无法连接网管，请检查设置的 网管IP、账号、密码 是否正确')
                    print (u'请检查内网路由是否设置成功')
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
        while True:
            sleep(3)
            try:
                ret = self.chan.recv(65535)
                ret = ret.decode('utf-8')
            except:
                continue
            result += ret
            print((ret) )
            if '@zblteuas' in ret:
                break
            if '@qdlteuas' in ret:
                break
            if '@jnwuas' in ret:
                break
            if '@wfw1mas' in ret:
                break
        return result

#生成图片字体、大小、压缩比率
def gen_img(text, filename):
    a = Image.new('RGB',(1500,4000),'white')
    drw = ImageDraw.Draw(a)
    path = 'c:\\windows\\fonts\\msyh.ttf'
    if not os.path.exists(path):
        path = 'c:\\windows\\fonts\\SIMYOU.TTF'
        if not os.path.exists(path):
            path = 'c:\\windows\\fonts\\simsun.ttc'
    font=ImageFont.truetype(path,size=20)
    drw.text((10,10),text,font=font,fill='black')
    a.save(filename,quality=5)

#监听微信群，执行命令，返回微信群结果
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    if msg['Type'] == 'Text':
        datas = []
        content = msg['Text']
        source = msg['FromUserName']
        username = msg['ActualNickName']
        group = itchat.get_chatrooms(update=True)
        chatroom_id =  itchat.search_chatrooms()
        datas.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
                 '---'+ ':' + content +'\n')
        f = open('微信监视文件.txt','a+')  #在第一次运行时会自动创建文件

        f.writelines(datas)
        f.flush()
        print(datas)
        if content.startswith('##1##'):
            host.connect()
            #print(source)  #个人ID
            #print(username) #个人名字
            #print(group)   #群的所有信息
            #print(chatroom_id) #群的ID
            rets = host.send('amos '+ content[5:])
            rets += host.send('run ' + Command1)
            filename = 'myimg.jpg'
            gen_img(rets, filename)
            f.write(rets)
            f.flush()
            w = get_warnnings(rets)
            if w:
                itchat.send(rets, toUserName=msg['ToUserName'])
            #itchat.send(rets, toUserName=msg['ToUserName'])
            itchat.send_image(filename, toUserName=msg['ToUserName'])
            itchat.send_image(filename, toUserName=msg['FromUserName'])
            #itchat.send_image(filename, toUserName=msg['ActualNickName'])
            #itchat.send_image(filename, toUserName=itchat.get_chatrooms(update=True))
            #itchat.send_image(filename, toUserName=itchat.search_chatrooms()) #0

            host.close()
        if content.startswith('##2##'):
            host.connect()
            rets = host.send('amos '+ content[5:])
            rets += host.send('run ' + Command2)
            filename = 'myimg.jpg'
            gen_img(rets, filename)
            f.write(rets)
            f.flush()
            tem = rets.split('\n')[29]
            tem = [t for t in tem.split(' ') if t]
            itchat.send(tem[-2], toUserName=msg['ToUserName']) #0
            itchat.send(tem[-2], toUserName=msg['FromUserName']) #0
            itchat.send_image(filename, toUserName=msg['ToUserName'])
            itchat.send_image(filename, toUserName=msg['FromUserName'])
            #itchat.send_image(filename, toUserName=msg['ActualNickName'])
            #itchat.send_image(filename, toUserName=itchat.get_chatrooms(update=True)) #0
            #itchat.send_image(filename, toUserName=itchat.search_chatrooms())  #0

            host.close()
        if content.startswith('##3##'):
            host.connect()
            rets = host.send('amos '+ content[5:])
            rets += host.send('run ' + Command3)
            filename = 'myimg.jpg'
            gen_img(rets, filename)
            f.write(rets)
            f.flush()
            #itchat.send(rets, toUserName=msg['ToUserName']) #0
            itchat.send_image(filename, toUserName=msg['ToUserName'])
            itchat.send_image(filename, toUserName=msg['FromUserName'])
            #itchat.send_image(filename, toUserName=msg['ActualNickName'])
            #itchat.send_image(filename, toUserName=itchat.get_chatrooms(update=True)) #0
            #itchat.send_image(filename, toUserName=itchat.search_chatrooms())  #0
            host.close()
        if content.startswith('##4##'):
            host.connect()
            rets = host.send('amos '+ content[5:])
            rets += host.send('run ' + Command4)
            filename = 'myimg.jpg'
            gen_img(rets, filename)
            f.write(rets)
            f.flush()
            #itchat.send(rets, toUserName=msg['ToUserName']) #0
            itchat.send_image(filename, toUserName=msg['ToUserName'])
            itchat.send_image(filename, toUserName=msg['FromUserName'])
            #itchat.send_image(filename, toUserName=msg['ActualNickName'])
            #itchat.send_image(filename, toUserName=itchat.get_chatrooms(update=True)) #0
            #itchat.send_image(filename, toUserName=itchat.search_chatrooms())  #0
            host.close()

#读取百度网络时间和使用时间限制
def get_webservertime(host):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    dat="%u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="time %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    #print (dat)
    now_day = dat
    end_day ='2019-12-31'
    new_mow_day = time.strptime(now_day, "%Y-%m-%d")
    new_end_day = time.strptime(end_day, "%Y-%m-%d")
    if new_mow_day < new_end_day:
        print('已经连接互联网........OK...........')
    else:
       print('使用时间已经到期，联系邮箱：woguomingli@163.com')
       sys.exit()

if __name__ == '__main__':
    conf =  configparser.ConfigParser()
    conf.read("conf/configure.conf")    # 加载 conf文件夹下的mail.conf配置文件
    Serviceip = conf.get('message','Serviceip')
    Uname = conf.get('message','Uname')
    Upassword = conf.get('message','Upassword')
    Command1 = conf.get('message','Command1')
    Command2 = conf.get('message','Command2')
    Command3 = conf.get('message','Command3')
    Command4 = conf.get('message','Command4')

    get_webservertime('www.baidu.com')

    host = Linux(Serviceip,Uname, Upassword)

    itchat.auto_login(hotReload=True)
    print('微信监控器已开启........OK.........')
    itchat.run()
