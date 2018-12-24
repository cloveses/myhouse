# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'talkroom.ui'
#
# Created: Sun Sep 23 03:10:46 2018
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1041, 633)
        self.textEdit_talkuser = QtGui.QTextEdit(Form)
        self.textEdit_talkuser.setGeometry(QtCore.QRect(20, 30, 151, 491))
        self.textEdit_talkuser.setObjectName(_fromUtf8("textEdit_talkuser"))
        self.textEdit_talkall = QtGui.QTextEdit(Form)
        self.textEdit_talkall.setGeometry(QtCore.QRect(190, 30, 611, 371))
        self.textEdit_talkall.setObjectName(_fromUtf8("textEdit_talkall"))
        self.lineEdit_talk = QtGui.QLineEdit(Form)
        self.lineEdit_talk.setGeometry(QtCore.QRect(190, 420, 481, 101))
        self.lineEdit_talk.setObjectName(_fromUtf8("lineEdit_talk"))
        self.pushButton_talksend = QtGui.QPushButton(Form)
        self.pushButton_talksend.setGeometry(QtCore.QRect(673, 419, 131, 101))
        self.pushButton_talksend.setObjectName(_fromUtf8("pushButton_talksend"))
        self.label_giftimg = QtGui.QLabel(Form)
        self.label_giftimg.setGeometry(QtCore.QRect(840, 370, 151, 111))
        self.label_giftimg.setText(_fromUtf8(""))
        self.label_giftimg.setObjectName(_fromUtf8("label_giftimg"))
        self.checkBox_flower = QtGui.QCheckBox(Form)
        self.checkBox_flower.setGeometry(QtCore.QRect(850, 30, 91, 19))
        self.checkBox_flower.setObjectName(_fromUtf8("checkBox_flower"))
        self.checkBox_car = QtGui.QCheckBox(Form)
        self.checkBox_car.setGeometry(QtCore.QRect(850, 100, 91, 19))
        self.checkBox_car.setObjectName(_fromUtf8("checkBox_car"))
        self.checkBox_rocket = QtGui.QCheckBox(Form)
        self.checkBox_rocket.setGeometry(QtCore.QRect(850, 170, 91, 19))
        self.checkBox_rocket.setObjectName(_fromUtf8("checkBox_rocket"))
        self.checkBox_beauty = QtGui.QCheckBox(Form)
        self.checkBox_beauty.setGeometry(QtCore.QRect(850, 240, 91, 19))
        self.checkBox_beauty.setObjectName(_fromUtf8("checkBox_beauty"))
        self.pushButton_giftsend = QtGui.QPushButton(Form)
        self.pushButton_giftsend.setGeometry(QtCore.QRect(850, 290, 91, 51))
        self.pushButton_giftsend.setObjectName(_fromUtf8("pushButton_giftsend"))
        self.label_giftuser = QtGui.QLabel(Form)
        self.label_giftuser.setGeometry(QtCore.QRect(840, 510, 151, 41))
        self.label_giftuser.setText(_fromUtf8(""))
        self.label_giftuser.setObjectName(_fromUtf8("label_giftuser"))
        self.label_username = QtGui.QLabel(Form)
        self.label_username.setGeometry(QtCore.QRect(500, 570, 151, 16))
        self.label_username.setText(_fromUtf8(""))
        self.label_username.setObjectName(_fromUtf8("label_username"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_talksend, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.clicked_talksend)
        QtCore.QObject.connect(self.pushButton_giftsend, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.clicked_giftsend)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "talkroom", None))
        self.pushButton_talksend.setText(_translate("Form", "发送", None))
        self.checkBox_flower.setText(_translate("Form", "鲜花", None))
        self.checkBox_car.setText(_translate("Form", "汽车", None))
        self.checkBox_rocket.setText(_translate("Form", "火箭", None))
        self.checkBox_beauty.setText(_translate("Form", "美女", None))
        self.pushButton_giftsend.setText(_translate("Form", "送礼物", None))

