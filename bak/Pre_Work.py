# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pre_Work.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Pre_Work_Form(object):
    def setupUi(self, Pre_Work_Form):
        Pre_Work_Form.setObjectName("Pre_Work_Form")
        Pre_Work_Form.resize(806, 541)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("文件预备.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Pre_Work_Form.setWindowIcon(icon)
        self.pushButton_xml2csv = QtWidgets.QPushButton(Pre_Work_Form)
        self.pushButton_xml2csv.setGeometry(QtCore.QRect(590, 80, 100, 40))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        self.pushButton_xml2csv.setFont(font)
        self.pushButton_xml2csv.setObjectName("pushButton_xml2csv")
        self.pushButton_csv2rec = QtWidgets.QPushButton(Pre_Work_Form)
        self.pushButton_csv2rec.setGeometry(QtCore.QRect(590, 340, 100, 40))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        self.pushButton_csv2rec.setFont(font)
        self.pushButton_csv2rec.setObjectName("pushButton_csv2rec")
        self.groupBox = QtWidgets.QGroupBox(Pre_Work_Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 571, 171))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_getxmlpath = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_getxmlpath.setGeometry(QtCore.QRect(510, 60, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_getxmlpath.setFont(font)
        self.pushButton_getxmlpath.setObjectName("pushButton_getxmlpath")
        self.pushButton_getcsvpath = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_getcsvpath.setGeometry(QtCore.QRect(510, 120, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_getcsvpath.setFont(font)
        self.pushButton_getcsvpath.setObjectName("pushButton_getcsvpath")
        self.lineEdit_xmlpath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_xmlpath.setGeometry(QtCore.QRect(20, 60, 471, 31))
        self.lineEdit_xmlpath.setObjectName("lineEdit_xmlpath")
        self.lineEdit_csvpath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_csvpath.setGeometry(QtCore.QRect(20, 120, 471, 31))
        self.lineEdit_csvpath.setObjectName("lineEdit_csvpath")
        self.groupBox_2 = QtWidgets.QGroupBox(Pre_Work_Form)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 200, 571, 321))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 130, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(20, 250, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.pushButton_getcsvpath_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_getcsvpath_2.setGeometry(QtCore.QRect(510, 150, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_getcsvpath_2.setFont(font)
        self.pushButton_getcsvpath_2.setObjectName("pushButton_getcsvpath_2")
        self.pushButton_getrecpath = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_getrecpath.setGeometry(QtCore.QRect(510, 270, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_getrecpath.setFont(font)
        self.pushButton_getrecpath.setObjectName("pushButton_getrecpath")
        self.lineEdit_csvpath_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_csvpath_2.setGeometry(QtCore.QRect(20, 150, 471, 31))
        self.lineEdit_csvpath_2.setObjectName("lineEdit_csvpath_2")
        self.lineEdit_recpath = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_recpath.setGeometry(QtCore.QRect(20, 270, 471, 31))
        self.lineEdit_recpath.setObjectName("lineEdit_recpath")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(20, 190, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.lineEdit_imagepath = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_imagepath.setGeometry(QtCore.QRect(20, 210, 471, 31))
        self.lineEdit_imagepath.setObjectName("lineEdit_imagepath")
        self.pushButton_getimagepath = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_getimagepath.setGeometry(QtCore.QRect(510, 210, 41, 28))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_getimagepath.setFont(font)
        self.pushButton_getimagepath.setObjectName("pushButton_getimagepath")
        self.lineEdit_label_num = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_label_num.setGeometry(QtCore.QRect(20, 50, 121, 31))
        self.lineEdit_label_num.setObjectName("lineEdit_label_num")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.textEdit_labels = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_labels.setGeometry(QtCore.QRect(200, 40, 291, 81))
        self.textEdit_labels.setObjectName("textEdit_labels")
        self.groupBox.raise_()
        self.pushButton_xml2csv.raise_()
        self.pushButton_csv2rec.raise_()
        self.groupBox_2.raise_()

        self.retranslateUi(Pre_Work_Form)
        self.pushButton_getxmlpath.clicked.connect(Pre_Work_Form.get_xml_path)
        self.pushButton_getcsvpath.clicked.connect(Pre_Work_Form.get_csv_path)
        self.pushButton_getcsvpath_2.clicked.connect(Pre_Work_Form.get_csv_path2)
        self.pushButton_getrecpath.clicked.connect(Pre_Work_Form.get_rec_path)
        self.pushButton_xml2csv.clicked.connect(Pre_Work_Form.xml_to_csv)
        self.pushButton_csv2rec.clicked.connect(Pre_Work_Form.csv_to_rec)
        self.pushButton_getimagepath.clicked.connect(Pre_Work_Form.get_image_path)
        QtCore.QMetaObject.connectSlotsByName(Pre_Work_Form)

    def retranslateUi(self, Pre_Work_Form):
        _translate = QtCore.QCoreApplication.translate
        Pre_Work_Form.setWindowTitle(_translate("Pre_Work_Form", "Pre-Work"))
        self.pushButton_xml2csv.setText(_translate("Pre_Work_Form", "1.XML转CSV"))
        self.pushButton_csv2rec.setText(_translate("Pre_Work_Form", "2.CSV转REC"))
        self.groupBox.setTitle(_translate("Pre_Work_Form", "xml_to_csv"))
        self.label.setText(_translate("Pre_Work_Form", "XML所在目录："))
        self.label_5.setText(_translate("Pre_Work_Form", "输出CSV目录："))
        self.pushButton_getxmlpath.setText(_translate("Pre_Work_Form", "设置"))
        self.pushButton_getcsvpath.setText(_translate("Pre_Work_Form", "设置"))
        self.groupBox_2.setTitle(_translate("Pre_Work_Form", "generate_tfrecord"))
        self.label_2.setText(_translate("Pre_Work_Form", "CSV所在目录："))
        self.label_8.setText(_translate("Pre_Work_Form", "输出REC目录："))
        self.pushButton_getcsvpath_2.setText(_translate("Pre_Work_Form", "设置"))
        self.pushButton_getrecpath.setText(_translate("Pre_Work_Form", "设置"))
        self.label_9.setText(_translate("Pre_Work_Form", "图片样本所在目录："))
        self.pushButton_getimagepath.setText(_translate("Pre_Work_Form", "设置"))
        self.label_3.setText(_translate("Pre_Work_Form", "检测对象数："))
