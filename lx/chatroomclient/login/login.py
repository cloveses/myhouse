# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Fri Sep 21 16:07:53 2018
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
        Form.resize(530, 410)
        self.lineEdit_username = QtGui.QLineEdit(Form)
        self.lineEdit_username.setGeometry(QtCore.QRect(150, 200, 221, 41))
        self.lineEdit_username.setObjectName(_fromUtf8("lineEdit_username"))
        self.lineEdit_passwd = QtGui.QLineEdit(Form)
        self.lineEdit_passwd.setGeometry(QtCore.QRect(150, 270, 221, 41))
        self.lineEdit_passwd.setObjectName(_fromUtf8("lineEdit_passwd"))
        self.lable_username = QtGui.QLabel(Form)
        self.lable_username.setGeometry(QtCore.QRect(70, 210, 72, 15))
        self.lable_username.setObjectName(_fromUtf8("lable_username"))
        self.label_passwd = QtGui.QLabel(Form)
        self.label_passwd.setGeometry(QtCore.QRect(70, 280, 72, 15))
        self.label_passwd.setObjectName(_fromUtf8("label_passwd"))
        self.pushButton_login = QtGui.QPushButton(Form)
        self.pushButton_login.setGeometry(QtCore.QRect(150, 340, 101, 41))
        self.pushButton_login.setObjectName(_fromUtf8("pushButton_login"))
        self.pushButton_register = QtGui.QPushButton(Form)
        self.pushButton_register.setGeometry(QtCore.QRect(270, 340, 101, 41))
        self.pushButton_register.setObjectName(_fromUtf8("pushButton_register"))
        self.label_logo = QtGui.QLabel(Form)
        self.label_logo.setGeometry(QtCore.QRect(0, 0, 531, 141))
        self.label_logo.setText(_fromUtf8(""))
        self.label_logo.setObjectName(_fromUtf8("label_logo"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_register, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_register)
        QtCore.QObject.connect(self.pushButton_login, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_login)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.lable_username.setText(_translate("Form", "用户名：", None))
        self.label_passwd.setText(_translate("Form", "密  码：", None))
        self.pushButton_login.setText(_translate("Form", "登录", None))
        self.pushButton_register.setText(_translate("Form", "注册", None))

