import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from scan import *
class start(QMainWindow,Ui_Form):
	def __init__(self,parent=None):
		super().__init__(parent)
		self.setupUi(self)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = start()
	myWin.show()
	sys.exit(app.exec_())