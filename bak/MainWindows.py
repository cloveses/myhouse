##-----以下为VideoInfor主窗口的class-----##
class Ui_MainWindow(QMainWindow, Ui_MainWindow):   #第一个Ui_MainWindow名称可自定义，全篇统一即可；第二个Ui_MainWindow确定源于VideoInfor的class名
    def __init__(self, parent=None):   #parent不知用法，删除会报错
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)

    ##-----以下为pushButton_opencam功能，打开摄像头-----##
    def open_camera(self):

        # This is needed since the notebook is stored in the object_detection folder.
        sys.path.append("..")

        # Import utilites
        from utils import label_map_util
        from utils import visualization_utils as vis_util

        # Name of the directory containing the object detection module we're using
        MODEL_NAME = '~~train\ssd_mobilenet_v1_pets'
        VIDEO_NAME = 'test.mov'

        # Grab path to 上一级目录
        CWD_PATH = os.path.dirname(os.getcwd())
        LABELS_PATH = '~~outcome'

        # Path to frozen detection graph .pb file, which contains the model that is used
        # for object detection.
        PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH, LABELS_PATH, 'label_map.pbtxt')

        # Path to video
        PATH_TO_VIDEO = os.path.join(os.getcwd(), VIDEO_NAME)
        # Number of classes the object detector can identify
        NUM_CLASSES = 6

        # Load the label map.
        # Label maps map indices to category names, so that when our convolution
        # network predicts `5`, we know that this corresponds to `king`.
        # Here we use internal utility functions, but anything that returns a
        # dictionary mapping integers to appropriate string labels would be fine
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            sess = tf.Session(graph=detection_graph)

        # Define input and output tensors (i.e. data) for the object detection classifier

        # Input tensor is the image
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # Open video file
        video = cv2.VideoCapture(0)

        while (video.isOpened()):

            # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
            # i.e. a single-column array, where each item in the column has the pixel RGB value
            ret, frame = video.read()
            frame_expanded = np.expand_dims(frame, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})

            # Draw the results of the detection (aka 'visulaize the results')
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.80)

            # All the results have been drawn on the frame, so it's time to display it.
            cv2.imshow('Press Space to Exit', frame)

            # Press '空格' to quit
            if cv2.waitKey(1) == ord(' '):
                break

        # Clean up
        video.release()
        cv2.destroyAllWindows()

        # # import cv2
        # # import numpy as np    #添加模块和矩阵模块
        # cap = cv2.VideoCapture(0)   #默认的摄像头，多个摄像头改为1、2、3，打开摄像头；若打开本地视频，同opencv一样，只需将0换成("×××.avi")
        # while (1):   # get a frame 或者用 while True
        #     ret, frame = cap.read()   # show a frame ，获取一帧
        #     cv2.imshow("Press Space to Exit", frame)
        #     if cv2.waitKey(1) & 0xFF == ord(' '):   #1表示延迟1ms接受键盘传来的‘q’，若为0，则第一章图片刷新后一直等待q的传来，若为1000，则每1s图像刷新一次
        #         break   #敲击“空格”关闭摄像头预览
        # cap.release()
        # cv2.destroyAllWindows()
    ##-----以上为pushButton_opencam功能，打开摄像头-----##

    ##-----以下为pushButton_startdetection功能，开始实时检测-----##
    def start_detection(self):
        # coding:utf-8
        import cv2
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        cap.set(1, 10.0)
        # 此处fourcc的在MAC上有效，如果视频保存为空，那么可以改一下这个参数试试, 也可以是-1
        fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
        # 第三个参数则是镜头快慢的，10为正常，小于10为慢镜头
        out = cv2.VideoWriter('/opt/code/video/output2.avi', fourcc, 10, (640, 480))
        while True:
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.flip(frame, 1)
                a = out.write(frame)
                cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            else:
                break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
    ##-----以上为pushButton_startdetection功能，开始实时检测-----##

    ##-----以下为pushButton_stopdetection功能，停止实时检测-----##
    def stop_detection(self):
        print("stop_detection")
        # import cv2
        # import numpy as np
        # image_backgroud = cv2.imread('O:\Grade_2017_Liu_Jinshan\Grogramming\PyCharm_File\Try1\images\test.jpg')
        # image_backgroud = cv2.cvtColor(image_backgroud, cv2.COLOR_BGR2GRAY)
        # # 选取关键点截图
        # liefeng1 = cv2.imread('D:\liefeng1.png', 0)
        # w, h = liefeng1.shape[::-1]
        # res = cv2.matchTemplate(image_backgroud, liefeng1, cv2.TM_CCOEFF_NORMED)
        # # 相似度
        # threshold = 0.3
        # loc = np.where(res > threshold)
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(image_backgroud, pt, (pt[0] + w, pt[1] + h), (155, 0, 0), 1)
        #
        # cv2.imshow('liefeng', image_backgroud)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    ##-----以上为pushButton_stopdetection功能，停止实时检测-----##

    ##-----以下为pushButton_closecam功能，关闭摄像头-----##
    def close_camera(self):
        print("close_camera")
    ##-----以上为pushButton_closecam功能，关闭摄像头-----##

    ##-----以下为pushButton_closecam功能，关闭摄像头-----##
    ##-----以上为pushButton_closecam功能，关闭摄像头-----##
##-----以上为VideoInfor主窗口的class-----##