import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# sess = tf.InteractiveSession()
# tf.global_variables_initializer().run()

def main(center_point = np.array((0,0)), square_len = 8.0):
    square_len = tf.constant(square_len)
    transf = np.array([[-1,1,1,-1],[1,1,-1,-1]])
    transf = tf.constant(transf.astype(np.float32))
    points = np.array([np.full((4,),center_point[0]), np.full((4,),center_point[0])])
    points = tf.constant(points.astype(np.float32))
    tr = tf.multiply(transf, square_len)
    pts = tf.add(points, tr)

    with tf.Session() as sess:
        res = sess.run(pts)

    return res

def test(i=0)
    center_point = np.array((0,0))
    square_len = 8.0
    results = [[],[]]
    res = None
    if i >=4:
        return results
    if not res:
        res = main(center_point, square_len):
        results[0].append(res[0])
        results[1].append(res[1])
    else:
        main()
