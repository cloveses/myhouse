#encoding=UTF-8
#Author:九零网安
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
from login_init import *
# from chat import *



#解释界面
class MyMainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
#逻辑        
    # def checklogin(self):
    #      if self.pushButton.clicked():
    @pyqtSlot()
    def on_pushButton_clicked(self):
            if self.textEdit.text() == 'admin':
                if self.textEdit_2.text() == '9090':
                    rely = QMessageBox.information(self, "提示", "登陆成功", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                    # print ( rely )
                    # self.window.setVisible(False)
                    # from1 = QtWidgets.SecondWindow()
                    # ui = SecondWindow1.Ui_SecondWindow()
                    # ui.setupUi(from1)
                    # from1.setVisible(True)
                    # # from1.exec_()
                    # self.window.show()
                    self.takeCentralWidget()
                    self.setup2Ui(self)
                else:
                    rely = QMessageBox.information(self,"提示","登陆失败", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                    print ( rely )
            else:
                rely = QMessageBox.information(self,"提示", "用户名错误", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                print ( rely )
    @pyqtSlot()
    def on_toolButton_Clicked():
# 设置代理
        proxy = QtNetwork.QNetworkProxy()
# Http访问代理
        proxy.setType=QtNetwork.QNetworkProxy.HttpProxy
# 代理ip地址HttpProxy
        proxy.setHostName("127.0.0.1")
# 端口号
        proxy.setPort(1080)
        proxy.setUser("4")
        proxy.setPassword("1")
        QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
