# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\职坐标\项目\20190101重新设计\manychat.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class manychat(object):
    def setupUi3(self, Form):
        Form.setObjectName("Form")
        Form.resize(754, 458)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(120, 40, 621, 291))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 72, 15))
        self.label.setObjectName("label")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 40, 101, 321))
        self.listView.setObjectName("listView")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 72, 15))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(120, 370, 531, 81))
        self.textEdit.setObjectName("textEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(670, 390, 72, 41))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 340, 72, 15))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 340, 72, 15))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(200, 340, 72, 15))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(360, 340, 111, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(480, 340, 111, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(610, 340, 41, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(20, 430, 81, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(20, 380, 72, 15))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(20, 400, 72, 15))
        self.label_12.setObjectName("label_12")
        self.setWindowTitle("九零网安多人聊天模式")
        self.retranslateUi3(self.centralwidget)
        Form.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self.centralwidget)

    def retranslateUi3(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "在线列表"))
        self.label_2.setText(_translate("Form", "消息列表"))
        self.label_3.setText(_translate("Form", "发送"))
        self.label_4.setText(_translate("Form", "发送文件"))
        self.label_5.setText(_translate("Form", "语音聊天"))
        self.label_6.setText(_translate("Form", "屏幕分享"))
        self.label_7.setText(_translate("Form", "服务器删除记录"))
        self.label_8.setText(_translate("Form", "服务器文件管理"))
        self.label_9.setText(_translate("Form", "设置"))
        self.label_10.setText(_translate("Form", "Beta V1.0"))
        self.label_11.setText(_translate("Form", "九零网安"))
        self.label_12.setText(_translate("Form", "版权所有"))

