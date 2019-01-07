# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QWidget,QVBoxLayout,QMessageBox,QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPalette
from PyQt5.QtCore import pyqtSlot
from login import *
from manychat import *
import sys

class start(QMainWindow,Ui_Form,manychat):
	
	def __init__(self,parent=None):
		super().__init__(parent)
		self.setupUi(self)

	def redirect(self):
		file_object = open('1.txt','r')
		try: 
			if self.textEdit.toPlainText() in file_object:
				box = QMessageBox(QMessageBox.Information, "提示", "登陆成功")
				yes = box.addButton("是", QMessageBox.YesRole)
				
				no = box.addButton("否", QMessageBox.NoRole)
				box.exec_()
				# rely = QMessageBox.information(self, "提示", "登陆成功", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
				
				# print ( box.clickedButton() )
				if box.clickedButton() == yes:
					print('ddfggg')
					self.takeCentralWidget()#移除窗口中其他现有元素
					self.setupUi3(self)#建立新的界面元素
		finally:
			file_object.close()
	@pyqtSlot()
	def on_click(self):
		self.redirect()
"""
作者：翎月
链接：https://www.jianshu.com/p/d8168034917c
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
"""
"""
class many(QMainWindow,manychat):
	def __init__(self,parent=None):
		super().__init__(parent)
		self.setupUi(self)
"""
if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = start()
	w.show()
	sys.exit(app.exec_())