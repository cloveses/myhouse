#coding:utf-8
from PyQt4 import QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox
import sys
import imgshow
import threading
import os
import time
class Mywindow(QtGui.QWidget):
    def __init__(self):
        super(Mywindow, self).__init__()

class CTest(QObject):
    sinout = pyqtSignal()
    def __init__(self):
        super(CTest, self).__init__()
        self.sinout.connect(self.fuck)

    def fashe(self):
        self.sinout.emit()

    def createwindow(self):
        self.windowapp = QtGui.QApplication(sys.argv)
        self.mywindow = Mywindow()
        self.mywindow.show()
        self.windowapp.exec_()

    def fuck(self):
        print "cisss"
       # QMessageBox.information(None, u"错误警告", u"操")

#app = QCoreApplication(sys.argv)
tt = CTest()
tt.fashe()
# tt.createwindow()
# del tt.mywindow
#tt.fuck()

