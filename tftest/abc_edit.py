# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image and video
"""

import colorsys
import os
import time
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from add_box import add_box

import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from PIL import Image

from yolo3.model_multi import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import letterbox_image
from keras.utils import multi_gpu_model

from sort import *   #//////////////
import copy
import shutil

class YOLO(object):
    _defaults = {
        "model_path": 'model_data/yolo.h5',
        "anchors_path": 'model_data/yolo_anchors.txt',
        "classes_path": 'model_data/my-bag-data.txt',   # 'model_data/coco_classes.txt',
        "score" : 0.3,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 1,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults) # set up default values
        self.__dict__.update(kwargs) # and update with user overrides
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            print(self.model_path, self.anchors_path, self.classes_path)
            print(self.yolo_model.layers[-1].output_shape[-1])
            print(num_anchors, len(self.yolo_model.output), num_classes)
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        if self.gpu_num>=2:
            self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou,
                video_ways=self.batch_size)
        return boxes, scores, classes


    def detect_images(self, images):
        batch_size = len(images)
        start = timer()

        image_datas = []
        for image in images:
            if self.model_image_size != (None, None):
                assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
                assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
                boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
            else:
                new_image_size = (image.width - (image.width % 32),
                                  image.height - (image.height % 32))
                boxed_image = letterbox_image(image, new_image_size)
            image_data_one = np.array(boxed_image, dtype='float32')
            image_datas.append(image_data_one)
        end = timer()
        print(f"Resized {batch_size} images for {end-start} seconds")

        image_data = np.stack(image_datas)
        print(image_data.shape)
        image_data /= 255.

        start = timer()
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        end = timer()
        #print('out boxes are', out_boxes)
        #print('out boxes are', out_scores)
        #print('out boxes are', out_classes)
        print(f"Yolo3 processed {batch_size} images for {end-start} seconds")
        print('In this batch:')
        print(len(out_boxes))

        #for i in range(batch_size):
        #   print('Found {} boxes for {}'.format(out_boxes[i].shape[0], f'img{i}'))

        return out_boxes, out_scores, out_classes

    def close_session(self):
        self.sess.close()


def detect_img_batch(yolo, image_files, output_dir):
    images = []
    img_file_handles = []
    img_filenames = []
    for image_file in image_files:
        try:
            fh = open(image_file.path, 'rb')
            img_file_handles.append(fh)
            image = Image.open(fh)
            img_filenames.append(image_file.path.split("/")[-1])
        except Exception as e:
            print(e)
            print('Failed to open image' + image_file.path)
        else:
            images.append(image)
    out_infos = yolo.detect_images(images)
    out_boxes_, out_scores_, out_classes_ = out_infos
    for i, (img_fn, image) in enumerate(zip(img_filenames, images)):
        out_boxes = out_boxes_[i]
        out_scores = out_scores_[i]
        out_classes = out_classes_[i]
        img_out = add_box(image, out_boxes, out_scores, out_classes)
        img_out.save(output_dir + '/' + img_fn,"JPEG")

    for fh in img_file_handles:
        fh.close()

    for image_file in image_files:
        try:
            os.remove(image_file)
        except Exception as e:
            print(e)
            print('Failed to delete image' + image_file.path)
    return out_infos


def detect_img(yolo, output_dir, image_file, display_window):
    try:
        image = Image.open(image_file.path)
    except:
        print('Failed to open image' + image_file.path)
    else:
        file_name = image_file.name.split('.')[0] + '.png'
        try:
            r_image = yolo.detect_image(image)
            r_image.save(output_dir + '/' + file_name,"PNG")
        except:
            print('Failed to detect or save image ' + image_file.path)
        else:
            small_size = tuple(int(i/8) for i in r_image.size)
            display_img = r_image.resize(small_size, Image.ANTIALIAS)
            display_window.set_array(display_img)
            os.remove(image_file)

def watch_dir(pro_obj, yolo, out_dir, watch_dir, freq, batch_size, visualize):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    display_window = ax.imshow(np.random.rand(128, 128))
    plt.show(block=False)
    image_batch = []
    mot_tracker = Sort()  # //////////////
    def parse_filename(item):
        try:
            return int(item.name.split('.')[0])
        except Exception as e:
            print("Error occured when parsing this file:")
            num = item.name.split('.')[0]
            try:
                int(num)
            except Exception as e:
                print("The file name should start with an number")
                print(f"But it is '{num}'")
                raise e
            raise e
    round1 = True
    while True:
        while not pro_obj.is_run_or_stop():
            # 进入空循环，这里用堵塞代替    ִprocess tail
            ########################################
            if not round1:
                length = len(os.listdir(watch_dir))                                                             # fill 100 files with last copy
                if length != 0:
                    oldfilename = sorted(os.listdir(watch_dir), key=lambda x: int(x.split(".")[0]))[length - 1]
                    length_range = 100 - length % 100
                    if length_range != 100 and length > 0:
                        for i in range(length_range):
                            filename = str(i + int(oldfilename.split(".")[0]) + 1) + ".jpg"
                            shutil.copyfile(os.path.join(watch_dir, oldfilename), os.path.join(watch_dir, filename))  # fill end
                    with os.scandir(watch_dir) as it:
                        it_sort = sorted(it, key=parse_filename)
                        start_pos = 0
                        if image_batch != []:                       # find index not duplicate
                            a = int(parse_filename(it_sort[0]))
                            lastfile = int(parse_filename(image_batch[-1]))
                            if lastfile >= a:
                                start_pos = lastfile - a + 1
                            else:
                                start_pos = 0
                        for dir_entry in it_sort[start_pos:]:
                            fname = dir_entry.name
                            ext = fname.split('.')[-1]
                            if ext in ['jpg', 'png']:
                                image_batch.append(dir_entry)
                            else:
                                print('Unsuported file type ' + fname)
                    while len(image_batch) >= batch_size:
                        print(image_batch)
                        print(image_batch[:batch_size])
                        out_infos = detect_img_batch(yolo, image_batch[:batch_size], out_dir)
                        for i_box in range(len(out_infos[0])):
                            detections = np.hstack((out_infos[0][i_box], out_infos[1][i_box].reshape(-1, 1)))
                            # convert out_infos//////////////
                            if image_batch[i_box].name == '13_frame_173.jpg':
                                print('enter update()', i_box)
                            track_bbs_ids, bag_num = mot_tracker.update(detections)  # //////////////
                            print('image ', image_batch[i_box].name, '   Found', out_infos[0][i_box].shape[0], 'boxes  ',
                                  'bag number', bag_num)  # //////////////
                            pro_obj.putinto_queue(image_batch[i_box].name, bag_num)  # ----------
                        image_batch = image_batch[batch_size:]
                        print(image_batch)
            ########################################
            pro_obj.switch_lock.wait()  # ---------
        round1 = False
        n_files = 0
        with os.scandir(watch_dir) as it:
            it_sort = sorted(it, key=parse_filename)  #
            start_pos = 0
            if image_batch != []:
                a = int(parse_filename(it_sort[0]))
                lastfile = int(parse_filename(image_batch[-1]))
                if lastfile >= a:
                    start_pos = lastfile - a + 1
                else:
                    start_pos = 0
            for dir_entry in it_sort[start_pos:]:
                n_files += 1
                fname = dir_entry.name
                ext = fname.split('.')[-1]
                if ext in ['jpg', 'png']:
                    image_batch.append(dir_entry)
                else:
                    print('Unsuported file type ' + fname)

        while len(image_batch) >= batch_size:
            print(image_batch)
            print(image_batch[:batch_size])
            out_infos = detect_img_batch(yolo, image_batch[:batch_size], out_dir)
            for i_box in range(len(out_infos[0])):
                detections = np.hstack((out_infos[0][i_box], out_infos[1][i_box].reshape(-1, 1)))
                # convert out_infos//////////////
                # if image_batch[i_box].name == '13_frame_173.jpg':
                    # print('enter update()', i_box)
                track_bbs_ids, bag_num = mot_tracker.update(detections)  #//////////////
                print('image ', image_batch[i_box].name, '   Found', out_infos[0][i_box].shape[0], 'boxes  ',
                      'bag number', bag_num)  # //////////////

                pro_obj.putinto_queue(image_batch[i_box].name, bag_num)  # ----------

            image_batch = image_batch[batch_size:]
            print(image_batch)
        time.sleep(1/freq)
        if n_files == 0:
            print("No files in directory, waiting..")
    yolo.close_session()


def main_run(pro_obj):
    yolo_ = YOLO(
        model_path='logs/001/trained_weights_final.h5',
        classes_path='model_data/my-bag-data.txt',
        batch_size=100,
        gpu_num=1
    )
    watch_dir(
        pro_obj,
        yolo=yolo_,
        out_dir='output',
        watch_dir='/mnt/ramdisk/',
        freq=1,
        batch_size=100,
        visualize=True
    )    # watch_dir='input_images',
