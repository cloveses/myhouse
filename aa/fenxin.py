import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 获取某每次运行时喂给的数据。
# 由中心点的坐标和边长生成用于得出其四角点坐标的参数
def get_params_iter(square_len=1.0, x=0.0, y=0.0):
    # 用于从中心点变换四个点的单位矩阵
    transf = np.array([[-1.0,1.0,1.0,-1.0],[1.0,1.0,-1.0,-1.0]])
    # 将中心点坐标扩展为4个角点x和y坐标
    points = np.array([np.full((4,),x), np.full((4,),y)])
    return square_len, transf, points

# 将正方形的四角的四个点坐标数据变换为列表，
# 并在末尾添加首个列表元素（画出完整正方形）
def get_xys(xs,ys):
    x = list(xs[:])
    y = list(ys[:])
    x.append(x[0])
    y.append(y[0])
    return x,y
# 迭代次数
times = 5
square_len_num = 1.0

xs = None
ys = None

# 定义占位数据
square_len = tf.placeholder(tf.float32)
transf = tf.placeholder(tf.float32)
points = tf.placeholder(tf.float32)

s, t, p = get_params_iter()

# 定义计算图
tr = tf.multiply(transf, square_len)
pts = tf.add(points, tr)

with tf.Session() as sess:
    for i in range(times):
        # 计算首个正方形对应坐标数据
        if xs is None:
            res = sess.run(pts, feed_dict={square_len:s, transf:t, points:p})
            xs, ys = res
            plt.plot(*get_xys(xs, ys), 'g')
        else:
            temp_xs, temp_ys = [], []
            # 循环求出各顶点对应正方形的顶点坐标
            for x,y in zip(xs,ys):
                s, t, p = get_params_iter(square_len_num, x, y)
                # 喂入数据，计算各正方形顶点坐标
                res = sess.run(pts, feed_dict={square_len:s, transf:t, points:p})
                plt.plot(*get_xys(res[0], res[1]), 'g')
                temp_xs.extend(res[0])
                temp_ys.extend(res[1])
            xs = temp_xs
            ys = temp_ys
        # 边长减半
        square_len_num /= 2

plt.show()