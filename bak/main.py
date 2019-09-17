from Learn_Train import Ui_Learn_Train_Form
from PyQt5.QtWidgets import QWidget,QApplication
import sys
import tensorflow as tf

##-----以下为Learn_Train二级窗口的class-----##
class Ui_Learn_Train_Form(QWidget, Ui_Learn_Train_Form):   #第一个Ui_Learn_Train_Form名称可自定义，全篇统一即可；第二个Ui_Learn_Train_Form确定源于Learn_Train的class名
    def __init__(self, parent=None):  #parent不知用法，删除会报错
        super(Ui_Learn_Train_Form, self).__init__(parent)
        self.setupUi(self)

    ##-----以下为pushButton_getmodelpath功能，确定迁移学习用的现有model的文件夹路径,进而提供.config文件路径-----##
    def get_config_path(self):
        config_path, filetype= QFileDialog.getOpenFileName(self,   #将选取的文件路径存入config_path
                                                       "打开.config文件",   #弹窗窗口标题为“打开路径”
                                                       "",   #弹窗的起始路径
                                                       " *.config" #;;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        print(config_path)   #打印config_path路径方面调试
        Con = self.lineEdit_configpath
        Con.setText(config_path)   #将路径显示在lineEdit_modelpath中
    ##-----以上为pushButton_getmodelpath功能，确定迁移学习用的现有model的文件夹路径,进而提供.config文件路径-----##

    ##-----以下为pushButton_gettrainpath功能，确定学习过程中产生文件的保存路径-----##
    def get_train_path(self):
        train_path = QFileDialog.getExistingDirectory(self,   #将选取的文件夹路径存入train_path
                                                       "打开储存训练过程文件路径",   #弹窗窗口标题为“打开路径”
                                                       "",   #弹窗的起始路径
                                                       #" *.xml;;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        print(train_path)   #打印train_path路径方面调试
        T = self.lineEdit_trainpath
        T.setText(train_path)    #将路径显示在lineEdit_trainpath中
    ##-----以上为pushButton_gettrainpath功能，确定学习过程中产生文件的保存路径-----##

    ##-----以下为pushButton_starttrain功能，开始学习-----##
    def start_train(self):
        print('start_train')

        import tensorflow as tf
        import numpy as np

        BATCH_SIZE = 8
        seed = 23455
        rng = np.random.RandomState(seed)
        X = rng.rand(32,2)
        Y = [[int((x0+x1)<1)] for x0,x1 in X]
        # print(X)
        # print(Y)

        x = tf.placeholder(tf.float32,shape=(None,2))
        y_ = tf.placeholder(tf.float32,shape=(None,1))

        w1 = tf.Variable(tf.random_normal([2,3], stddev=1, seed=1))
        w2 = tf.Variable(tf.random_normal([3,1], stddev=1, seed=1))

        a = tf.matmul(x,w1)
        y = tf.matmul(a,w2)

        loss = tf.reduce_mean(tf.square(y-y_))
        train_step = tf.train.GradientDescentOptimizer(0.001).minimize(loss)

        # train_step = tf.train.MomentumOptimizer(0.001, 0.9).minimize(loss)
        # train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

        with tf.Session() as sess:
            init_op = tf.global_variables_initializer()
            sess.run(init_op)
            print(sess.run(w1))
            print(sess.run(w2))
            STEPS = 5000
            for i in range(STEPS):
                start = (i * BATCH_SIZE) % 32
                end = start + BATCH_SIZE
                sess.run(train_step, feed_dict={x:X[start:end],y_:Y[start:end]})
                if i % 500 == 0:
                    total_loss = sess.run(loss, feed_dict={x:X, y_:Y})
                    print('loss:', total_loss)
            print(sess.run(w1))
            print(sess.run(w2))

    ##-----以上为pushButton_starttrain功能，开始学习-----##

    ##-----以下为pushButton_stoptrain功能，停止学习-----##
    def stop_train(self):
        print('stop_train')
    ##-----以下为pushButton_stoptrain功能，停止学习-----##
##-----以下为Learn_Train二级窗口的class-----##

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex = Ui_Learn_Train_Form()
    ex.show()
    sys.exit(app.exec_())