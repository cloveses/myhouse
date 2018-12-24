# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imgshow.ui'
#
# Created: Sun Sep 23 12:05:04 2018
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
        Form.resize(400, 300)
        self.label_img = QtGui.QLabel(Form)
        self.label_img.setGeometry(QtCore.QRect(220, 170, 141, 91))
        self.label_img.setObjectName(_fromUtf8("label_img"))
        self.textEdit_show = QtGui.QTextEdit(Form)
        self.textEdit_show.setGeometry(QtCore.QRect(60, 30, 141, 111))
        self.textEdit_show.setObjectName(_fromUtf8("textEdit_show"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_img.setText(_translate("Form", "TextLabel", None))

