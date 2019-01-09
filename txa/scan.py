# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\admin90\Desktop\漏洞扫描器by九零网安.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(859, 354)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("G:/picture/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(250, 70, 256, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "漏洞扫描-by 九零网安"))
        list = [1,2,3,5,6,7,8,9]
        self.textBrowser.text(_translate("Form",list[0],list[1])