#! /usr/bin/env python
# coding=utf-8
import cv2
import os,glob
import numpy as np
import core.utils as utils
import tensorflow as tf
import time

s1 = time.time()
def mul_image(watch_dir="./mnt/ramdisk", output_path='./output'):
    # 指定第一个文件夹的位置

    imageDir = os.path.abspath(watch_dir)

    # 通过glob.glob来获取第一个文件夹下，所有'.jpg'文件
    imageList = glob.glob(os.path.join(imageDir, '*.jpg'))
    # print(imageList)

    return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
    pb_file = "./yolov3_bag_100_v3.pb"
    graph = tf.Graph()
    return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)  # 读取刚刚变量

    with tf.Session(graph=graph) as sess:       # 要有这种思想，一个会话处理全部图片。
        for item in imageList:
            image_path      = item
            # print('item',item)
            end = "/"
            name = item[item.rfind(end):] # 获取图片文件名
            # print(name)
            num_classes     = 1
            input_size      = 416
            out =output_path + name

            original_image = cv2.imread(image_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            original_image_size = original_image.shape[:2]
            image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size]) #图片处理
            image_data = image_data[np.newaxis, ...]

            pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
            [return_tensors[1], return_tensors[2], return_tensors[3]],
                    feed_dict={ return_tensors[0]: image_data})

            pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                            np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                            np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0) #整合预测框


            bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.6) # 这一步是将所有可能的预测信息提取出来，主要是三类：坐标值，可能性，类别
            # print('bboxes:',bboxes)
            # bboxes: [[301.13088989 118.44700623 346.95623779 172.39486694   0.97461057   0]...]

            bboxes = utils.nms(bboxes, 0.7, method='nms') # 这一步是 将刚刚提取出来的信息进行筛选，返回最好的预测值，同样是三类。
            # print('bboxes:',bboxes)
            # bboxes: [array([105.31238556,  54.51167679, 282.53552246, 147.27146912, 0.99279714,   0.        ])]

            image = utils.draw_bbox(original_image, bboxes) # 这一步是把结果画到新图上面
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # 转换颜色通道
            cv2.imwrite(out, image) # 保存检测结果

save_many = mul_image()
s2 = time.time()
print('总用时：', s2 - s1)
