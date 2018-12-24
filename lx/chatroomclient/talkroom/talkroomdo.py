#coding:utf-8
import os
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QString
import talkroom

class Talkroom(QtGui.QWidget):
    def __init__(self, client, myname):
        super(Talkroom, self).__init__()
        self.__client = client  #窗口管理类
        self.__myname = myname  #当前进入聊天室的我自己的名字
        self.__giftmap = {"0":"flower.png", "1":"car.png", "2":"rocket.png", "3":"beauty.png"}
        self.__giftshowname = {"flower.png":u"鲜花", "car.png":u"跑车", "rocket.png":u"火箭", "beauty.png":u"美女"}

        self.__flaginroom = "inroom" #聊天室协议包body的进入房间flag
        self.__flagoutroom = "outroom"#聊天室协议包body的离开房间flag
        self.__flagtalk = "talk"#聊天室协议包body的聊天flag
        self.__flaggift = "gift"#聊天室协议包body的礼物flag
        self.__flagclose= "close"#聊天室协议包body的关闭聊天室flag

        self.__closestatus = "0"   #协议包body的content的关闭值
        self.__giftdir = os.path.join(os.path.dirname(__file__), "img") #礼物所在目录路径
        self.__talkroomui = talkroom.Ui_Form()
        self.__talkroomui.setupUi(self)
        self.inroom()  #登录成功发个包告诉聊天室成员我进来了

    # 统一聊天室窗口发送消息给窗口管理类
    def writetoclient(self, body, action):
        if not self.__client.readywrite(body):
            QMessageBox.information(None, u"错误警告", action)

    # 发送关闭聊天室信息
    def closeEvent(self, event):
        self.outroom()     #先告诉大家离开房间
        body = {"flag":self.__flagclose, "content":self.__closestatus}
        self.writetoclient(body, u"异常退出")

    # 发送离开房间信息
    def outroom(self):
        body = {"flag": self.__flagoutroom, "content": self.__myname}
        self.writetoclient(body, u"异常离开聊天室")

    # 发送进入房间信息
    def inroom(self):
        self.__talkroomui.label_username.setText(QString(u"我是：" + self.__myname))
        body = {"flag": self.__flaginroom, "content": self.__myname}
        self.writetoclient(body, u"进入聊天室失败")

    # 发送聊天信息
    def clicked_talksend(self):
        talkcontent = unicode(self.__talkroomui.lineEdit_talk.text())
        body = {"flag": self.__flagtalk, "content":talkcontent}
        self.writetoclient(body, u"发送聊天信息失败")
        self.__talkroomui.textEdit_talkall.append(QString(u"我说:" + talkcontent))

    # 发送礼物处理
    def getgift(self):
        flowercheck = self.__talkroomui.checkBox_flower.isChecked()
        carcheck = self.__talkroomui.checkBox_car.isChecked()
        rocketcheck = self.__talkroomui.checkBox_rocket.isChecked()
        beautycheck = self.__talkroomui.checkBox_beauty.isChecked()
        return [flowercheck, carcheck, rocketcheck, beautycheck]

    # 发送礼物
    def clicked_giftsend(self):
        giftcontent = []
        gifts = self.getgift()
        for index, gift in enumerate(gifts):
            if gift:giftcontent.append(str(index))
        body = {"flag": self.__flaggift, "content": giftcontent}
        self.writetoclient(body, u"发送礼物失败")

    # 接收礼物处理
    def dealGift(self, content):
        giftname = content[u"gift"]
        giftuser = content[u"name"]
        self.__talkroomui.label_giftuser.setText(QString(giftuser + u"送了一个"
                                                           + self.__giftshowname[self.__giftmap[giftname]]))
        img = QtGui.QPixmap(os.path.join(self.__giftdir, self.__giftmap[giftname]))   #从本地取出礼物
        scaled_img = img.scaled(self.__talkroomui.label_giftimg.size(), QtCore.Qt.KeepAspectRatio)
        self.__talkroomui.label_giftimg.setPixmap(scaled_img)

    # 接收进入房间处理
    def dealInroom(self, content):
        self.__talkroomui.textEdit_talkuser.clear()
        for loginuser in content[u"allnames"]:   #刷新登录用户列表
            self.__talkroomui.textEdit_talkuser.append(QString(loginuser))
        self.__talkroomui.textEdit_talkall.append(QString(u"系统消息：欢迎" + content[u"inname"] + u"进入聊天室"))

    # 接收离开房间处理
    def dealOutroom(self, content):
        self.__talkroomui.textEdit_talkuser.clear()
        outstause = u"正常离开聊天室"
        try:content[u"allnames"].remove(content[u"outname"]) # 去除离开聊天室的用户
        except:outstause = u"崩溃离开聊天室"

        for loginuser in content[u"allnames"]:               # 刷新登录用户列表
            self.__talkroomui.textEdit_talkuser.append(QString(loginuser))
        self.__talkroomui.textEdit_talkall.append(QString(u"系统消息：" + content[u"outname"] + outstause))

    # 接收聊天信息处理
    def dealTalk(self, content):
        self.__talkroomui.textEdit_talkall.append(QString((content[u'name']) + u"说:" + (content[u'talk'])))
