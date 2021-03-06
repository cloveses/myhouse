# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Learn_Train.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Learn_Train_Form(object):
    def setupUi(self, Learn_Train_Form):
        Learn_Train_Form.setObjectName("Learn_Train_Form")
        Learn_Train_Form.resize(600, 350)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("学习训练.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Learn_Train_Form.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(Learn_Train_Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 571, 171))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 40, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_getconfigpath = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_getconfigpath.setGeometry(QtCore.QRect(510, 60, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_getconfigpath.setFont(font)
        self.pushButton_getconfigpath.setObjectName("pushButton_getconfigpath")
        self.pushButton_gettrainpath = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_gettrainpath.setGeometry(QtCore.QRect(510, 120, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_gettrainpath.setFont(font)
        self.pushButton_gettrainpath.setObjectName("pushButton_gettrainpath")
        self.lineEdit_configpath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_configpath.setGeometry(QtCore.QRect(20, 60, 471, 31))
        self.lineEdit_configpath.setObjectName("lineEdit_configpath")
        self.lineEdit_trainpath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_trainpath.setGeometry(QtCore.QRect(20, 120, 471, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_trainpath.setFont(font)
        self.lineEdit_trainpath.setObjectName("lineEdit_trainpath")
        self.label_trainpath = QtWidgets.QLabel(self.groupBox)
        self.label_trainpath.setGeometry(QtCore.QRect(20, 100, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_trainpath.setFont(font)
        self.label_trainpath.setObjectName("label_trainpath")
        self.pushButton_starttrain = QtWidgets.QPushButton(Learn_Train_Form)
        self.pushButton_starttrain.setGeometry(QtCore.QRect(150, 275, 100, 40))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        self.pushButton_starttrain.setFont(font)
        self.pushButton_starttrain.setObjectName("pushButton_starttrain")
        self.pushButton_stoptrain = QtWidgets.QPushButton(Learn_Train_Form)
        self.pushButton_stoptrain.setGeometry(QtCore.QRect(350, 275, 100, 40))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        self.pushButton_stoptrain.setFont(font)
        self.pushButton_stoptrain.setObjectName("pushButton_stoptrain")
        self.label_trainstep = QtWidgets.QLabel(Learn_Train_Form)
        self.label_trainstep.setGeometry(QtCore.QRect(30, 190, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_trainstep.setFont(font)
        self.label_trainstep.setObjectName("label_trainstep")
        self.lineEdit_trainstep = QtWidgets.QLineEdit(Learn_Train_Form)
        self.lineEdit_trainstep.setGeometry(QtCore.QRect(30, 210, 471, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_trainstep.setFont(font)
        self.lineEdit_trainstep.setObjectName("lineEdit_trainstep")

        self.retranslateUi(Learn_Train_Form)
        self.pushButton_getconfigpath.clicked.connect(Learn_Train_Form.get_config_path)
        self.pushButton_gettrainpath.clicked.connect(Learn_Train_Form.get_train_path)
        self.pushButton_starttrain.clicked.connect(Learn_Train_Form.start_train)
        self.pushButton_stoptrain.clicked.connect(Learn_Train_Form.stop_train)
        QtCore.QMetaObject.connectSlotsByName(Learn_Train_Form)

    def retranslateUi(self, Learn_Train_Form):
        _translate = QtCore.QCoreApplication.translate
        Learn_Train_Form.setWindowTitle(_translate("Learn_Train_Form", "Form"))
        self.groupBox.setTitle(_translate("Learn_Train_Form", "文件目录"))
        self.label_5.setText(_translate("Learn_Train_Form", "模型.config目录："))
        self.pushButton_getconfigpath.setText(_translate("Learn_Train_Form", "设置"))
        self.pushButton_gettrainpath.setText(_translate("Learn_Train_Form", "设置"))
        self.label_trainpath.setText(_translate("Learn_Train_Form", "训练过程文件储存目录："))
        self.pushButton_starttrain.setText(_translate("Learn_Train_Form", "开始训练"))
        self.pushButton_stoptrain.setText(_translate("Learn_Train_Form", "停止训练"))
        self.label_trainstep.setText(_translate("Learn_Train_Form", "当前训练步数："))

