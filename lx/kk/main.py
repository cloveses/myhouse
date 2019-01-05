# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPalette
from PyQt5.QtCore import pyqtSlot
from login import *
import sys

class start(QMainWindow,Ui_Form):
	def __init__(self,parent=None):
		super().__init__(parent)
		self.setupUi(self)
		file_object = open('1.txt','r')
		try: 
			if self.textEdit.text in file_object:
				print('登陆成功')
		finally:
			file_object.close()
"""
作者：翎月
链接：https://www.jianshu.com/p/d8168034917c
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
"""
if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = start()
	w.show()
	sys.exit(app.exec_())