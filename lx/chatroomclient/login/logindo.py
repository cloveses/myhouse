#coding:utf-8
import os
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtGui import QMessageBox
import login
'''
对客户端发送的协议包内容（body)：{"flag":"login", "content":{"name":name, "passwd":passwd}} 
例子：{"flag":"login", "content":{"name":"钟河东", "passwd":"11"}} 
登录成功的话，服务器返回：{"flag":"login", "content":"0"} 
登录密码失败，服务器返回：{"flag":"login", "content":"1"} 
登录用户名失败，服务器返回：{"flag":"login", "content":"2"} 
重复登录，服务器返回：{"flag":"login", "content":"3"} 
'''
class Login(QtGui.QWidget):
    def __init__(self, client, windowok, myname):
        super(Login, self).__init__()
        self.__client = client     # 窗口管理类
        self.__windowok = windowok # 窗口管理需要知道的登录框状态
        self.__myname = myname     # 窗口管理类需要知道的登录成功的名字
        self.__loginflag = "login" # 登录框协议包body的点击登录flag
        self.__closeflag = "close" # 登录框协议包body的点击关闭flag
        self.__closestatus = "1"   # 登录框协议包body的点击关闭content
        self.__loginsuc = "0"      # 服务器返回的body的content登录成功
        self.__passwderror = "1"   # 服务器返回的body的content密码错误
        self.__usernameerror = "2" # 服务器返回的body的content用户名错误
        self.__loginrepeat = "3"   # 服务器返回的body的content重复登录

        self.__loginui = login.Ui_Form()
        self.__loginui.setupUi(self)
        self.__loginlogodir = os.path.join(os.path.dirname(__file__), "img") #登录框上方图片路径
        self.__loginlogoname = "loginlogo.png"          #登录框上方图片名字
        self.__loginlogopath = os.path.join(self.__loginlogodir, self.__loginlogoname)
        self.setloginlogo() #登录框出现设置上方显示图片

    # 设置登录框上方图片
    def setloginlogo(self):
        self.__loginui.label_logo.setPixmap(QPixmap(self.__loginlogopath))

    # 统一登录窗口发送消息给窗口管理类
    def writetoclient(self, body, action):#
        if not self.__client.readywrite(body):
            QMessageBox.information(None, u"错误警告", action)

    # 处理登录窗口登录成功关闭和直接退出关闭
    def closeEvent(self, event):
        if self.__windowok[0] == False:
            body = {"flag":self.__closeflag, "content":self.__closestatus}
            self.writetoclient(body, "关闭登录框发送信息失败")

    # 窗口登录成功
    def suc_login(self):
        self.__windowok[0] = True
        self.close()

    # 接收登录信息处理
    def dealLogin(self, content):
        if content == self.__loginsuc: #登录成功
            self.suc_login()
        if content == self.__passwderror:
            QMessageBox.information(None, u"错误警告", u"密码错误")
        if content == self.__usernameerror:
            QMessageBox.information(self, u"错误警告", u"用户名错误")
        if content == self.__loginrepeat:
            QMessageBox.information(self, u"错误警告", u"重复登录")

    # 点击登录
    def click_login(self):
        username = unicode(self.__loginui.lineEdit_username.text())#把QString类型转为unicode
        passwd = unicode(self.__loginui.lineEdit_passwd.text())
        self.__myname[0] = username
        body = {"flag":self.__loginflag, "content":{"name":username, "passwd":passwd}}
        self.writetoclient(body, "登录信息发送失败")

    # 处理注册（自己写）
    def click_register(self):
        print "register fuck"



