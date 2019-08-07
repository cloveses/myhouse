import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def get_params_iter(square_len=1.0, x=0.0, y=0.0):
    transf = np.array([[-1.0,1.0,1.0,-1.0],[1.0,1.0,-1.0,-1.0]])
    points = np.array([np.full((4,),x), np.full((4,),y)])
    return square_len, transf, points

def get_xys(xs,ys):
    x = list(xs[:])
    y = list(ys[:])
    x.append(x[0])
    y.append(y[0])
    return x,y

times = 5
square_len_num = 1.0

xs = None
ys = None

square_len = tf.placeholder(tf.float32)
transf = tf.placeholder(tf.float32)
points = tf.placeholder(tf.float32)
s, t, p = get_params_iter()

tr = tf.multiply(transf, square_len)
pts = tf.add(points, tr)

with tf.Session() as sess:
    for i in range(times):
        if xs is None:
            res = sess.run(pts, feed_dict={square_len:s, transf:t, points:p})
            xs, ys = res
            plt.plot(*get_xys(xs, ys))
        else:
            temp_xs, temp_ys = [], []
            for x,y in zip(xs,ys):
                s, t, p = get_params_iter(square_len_num, x, y)
                res = sess.run(pts, feed_dict={square_len:s, transf:t, points:p})
                plt.plot(*get_xys(res[0], res[1]))
                temp_xs.extend(res[0])
                temp_ys.extend(res[1])
            xs = temp_xs
            ys = temp_ys
        square_len_num /= 2

plt.show()