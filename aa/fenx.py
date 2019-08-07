import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# sess = tf.InteractiveSession()
# tf.global_variables_initializer().run()

# def main(center_point = np.array((0,0)), square_len = 8.0):
#     square_len = tf.constant(square_len)
#     transf = np.array([[-1,1,1,-1],[1,1,-1,-1]])
#     transf = tf.constant(transf.astype(np.float32))
#     points = np.array([np.full((4,),center_point[0]), np.full((4,),center_point[0])])
#     points = tf.constant(points.astype(np.float32))

#     tr = tf.multiply(transf, square_len)
#     pts = tf.add(points, tr)

#     with tf.Session() as sess:
#         res = sess.run(pts)

    # return res

# def test(i=0)
#     center_point = np.array((0,0))
#     square_len = 8.0
#     results = [[],[]]
#     res = None
#     if i >=4:
#         return results
#     if not res:
#         res = main(center_point, square_len):
#         results[0].append(res[0])
#         results[1].append(res[1])
#     else:
#         main()

# if __name__ == '__main__':
#     print(main())
def get_params(square_len=4.0, x=0.0, y=0.0):
    # print(square_len,x,y)
    square_len = tf.Variable(square_len)
    transf = np.array([[-1.0,1.0,1.0,-1.0],[1.0,1.0,-1.0,-1.0]])
    transf = tf.Variable(transf.astype(np.float32))
    points = np.array([np.full((4,),x), np.full((4,),y)])
    points = tf.Variable(points.astype(np.float32))
    return square_len, transf, points

def get_params_iter(square_len=1.0, x=0.0, y=0.0):
    # print(square_len,x,y)
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