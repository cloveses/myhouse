from multiprocessing import Process

##-----以下为Learn_Train二级窗口的class-----##
class Ui_Learn_Train_Form(QWidget, Ui_Learn_Train_Form):   #第一个Ui_Learn_Train_Form名称可自定义，全篇统一即可；第二个Ui_Learn_Train_Form确定源于Learn_Train的class名
    def __init__(self, parent=None):  #parent不知用法，删除会报错
        super(Ui_Learn_Train_Form, self).__init__(parent)
        self.setupUi(self)
        self.p = None

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
        train_dir = self.lineEdit_trainpath.text()
        pipeline_config_path = self.lineEdit_configpath.text()
        self.p = Process(target=mystart_train, args=(train_dir,pipeline_config_path))
        self.p.start()

        # 以下代码移到一个一新函数mystart_train中

        tf.logging.set_verbosity(tf.logging.INFO)


        # os.chdir('Z:\\Tensorflow_Google\\research\\object_detection')

        train_dir=self.lineEdit_trainpath.text()   #'Z:\\Tensorflow_Google\\research\\object_detection\\~~train\\ssd_mobilenet_v1_pets'
        pipeline_config_path=self.lineEdit_configpath.text()   #'Z:\\Tensorflow_Google\\research\\object_detection\\~~models\\ssd_mobilenet_v1_pets\\ssd_mobilenet_v1_pets.config'

        flags = tf.app.flags
        flags.DEFINE_string('master', '', 'Name of the TensorFlow master to use.')
        flags.DEFINE_integer('task', 0, 'task id')
        flags.DEFINE_integer('num_clones', 1, 'Number of clones to deploy per worker.')
        flags.DEFINE_boolean('clone_on_cpu', False,
                             'Force clones to be deployed on CPU.  Note that even if '
                             'set to False (allowing ops to run on gpu), some ops may '
                             'still be run on the CPU if they have no GPU kernel.')
        flags.DEFINE_integer('worker_replicas', 1, 'Number of worker+trainer '
                                                   'replicas.')
        flags.DEFINE_integer('ps_tasks', 0,
                             'Number of parameter server tasks. If None, does not use '
                             'a parameter server.')
        flags.DEFINE_string('train_dir', train_dir,
                            'Directory to save the checkpoints and training summaries.')

        flags.DEFINE_string('pipeline_config_path', pipeline_config_path,
                            'Path to a pipeline_pb2.TrainEvalPipelineConfig config '
                            'file. If provided, other configs are ignored')

        flags.DEFINE_string('train_config_path', '',
                            'Path to a train_pb2.TrainConfig config file.')
        flags.DEFINE_string('input_config_path', '',
                            'Path to an input_reader_pb2.InputReader config file.')
        flags.DEFINE_string('model_config_path', '',
                            'Path to a model_pb2.DetectionModel config file.')

        FLAGS = flags.FLAGS

        @tf.contrib.framework.deprecated(None, 'Use object_detection/model_main.py.')
        def main():
            assert FLAGS.train_dir, '`train_dir` is missing.'
            if FLAGS.task == 0: tf.gfile.MakeDirs(FLAGS.train_dir)
            if FLAGS.pipeline_config_path:
                configs = config_util.get_configs_from_pipeline_file(
                    FLAGS.pipeline_config_path)
                if FLAGS.task == 0:
                    tf.gfile.Copy(FLAGS.pipeline_config_path,
                                  os.path.join(FLAGS.train_dir, 'pipeline.config'),
                                  overwrite=True)
            else:
                configs = config_util.get_configs_from_multiple_files(
                    model_config_path=FLAGS.model_config_path,
                    train_config_path=FLAGS.train_config_path,
                    train_input_config_path=FLAGS.input_config_path)
                if FLAGS.task == 0:
                    for name, config in [('model.config', FLAGS.model_config_path),
                                         ('train.config', FLAGS.train_config_path),
                                         ('input.config', FLAGS.input_config_path)]:
                        tf.gfile.Copy(config, os.path.join(FLAGS.train_dir, name),
                                      overwrite=True)

            model_config = configs['model']
            train_config = configs['train_config']
            input_config = configs['train_input_config']

            model_fn = functools.partial(
                model_builder.build,
                model_config=model_config,
                is_training=True)

            def get_next(config):
                return dataset_builder.make_initializable_iterator(
                    dataset_builder.build(config)).get_next()

            create_input_dict_fn = functools.partial(get_next, input_config)

            env = json.loads(os.environ.get('TF_CONFIG', '{}'))
            cluster_data = env.get('cluster', None)
            cluster = tf.train.ClusterSpec(cluster_data) if cluster_data else None
            task_data = env.get('task', None) or {'type': 'master', 'index': 0}
            task_info = type('TaskSpec', (object,), task_data)

            # Parameters for a single worker.
            ps_tasks = 0
            worker_replicas = 1
            worker_job_name = 'lonely_worker'
            task = 0
            is_chief = True
            master = ''

            if cluster_data and 'worker' in cluster_data:
                # Number of total worker replicas include "worker"s and the "master".
                worker_replicas = len(cluster_data['worker']) + 1
            if cluster_data and 'ps' in cluster_data:
                ps_tasks = len(cluster_data['ps'])

            if worker_replicas > 1 and ps_tasks < 1:
                raise ValueError('At least 1 ps task is needed for distributed training.')

            if worker_replicas >= 1 and ps_tasks > 0:
                # Set up distributed training.
                server = tf.train.Server(tf.train.ClusterSpec(cluster), protocol='grpc',
                                         job_name=task_info.type,
                                         task_index=task_info.index)
                if task_info.type == 'ps':
                    server.join()
                    return

                worker_job_name = '%s/task:%d' % (task_info.type, task_info.index)
                task = task_info.index
                is_chief = (task_info.type == 'master')
                master = server.target

            graph_rewriter_fn = None
            # if 'graph_rewriter_config' in configs:
            #   graph_rewriter_fn = graph_rewriter_builder.build(
            #       configs['graph_rewriter_config'], is_training=True)

            trainer.train(
                create_input_dict_fn,
                model_fn,
                train_config,
                master,
                task,
                FLAGS.num_clones,
                worker_replicas,
                FLAGS.clone_on_cpu,
                ps_tasks,
                worker_job_name,
                is_chief,
                FLAGS.train_dir,
                graph_hook_fn=graph_rewriter_fn)

        main()

    #-----以上为pushButton_starttrain功能，开始学习-----##

    #-----以下为pushButton_stoptrain功能，停止学习-----##
    def stop_train(self):
        print('stop_train')
        if self.p:
            self.p.terminate()
            self.p.join()
    ##-----以下为pushButton_stoptrain功能，停止学习-----##
##-----以下为Learn_Train二级窗口的class-----##

def mystart_train(train_dir,pipeline_config_path):
    pass



    def save_pb(self):
        print('start_train')
        # train_dir = self.lineEdit_trainpath.text()
        # pipeline_config_path = self.lineEdit_configpath.text()
        # self.p = Process(target=self.mystart_train, args=(train_dir,pipeline_config_path))
        # self.p.start()

        slim = tf.contrib.slim
        flags = tf.app.flags

        # config_path = 'Z:\\Tensorflow_Google\\research\\object_detection\\~~models\\ssd_mobilenet_v1_pets\\ssd_mobilenet_v1_pets.config'
        # Z: / Tensorflow_Google / research / object_detection / ~~train / ssd_mobilenet_v1_petsmodel.ckpt - 103699
        # checkpoint_prefix = 'Z:\\Tensorflow_Google\\research\\object_detection\\~~train\\ssd_mobilenet_v1_pets\\model.ckpt-103699'
        # output_directory = 'Z:\\Tensorflow_Google\\research\\object_detection\\~~train'

        config_path = self.lineEdit_configpath_2.text()
        checkpoint = self.lineEdit_trainpath_2.text()
        trainstep = self.lineEdit_trainstep.text()
        checkpoint_prefix = str(checkpoint) + '\\model.ckpt-' +str(trainstep)
        output_directory = self.lineEdit_pbpath.text()

        print(config_path)
        print(checkpoint)
        print(trainstep)
        print(checkpoint_prefix)
        print(output_directory)

        pass

        flags.DEFINE_string('input_type', 'image_tensor', 'Type of input node. Can be '
                                                          'one of [`image_tensor`, `encoded_image_string_tensor`, '
                                                          '`tf_example`]')
        flags.DEFINE_string('input_shape', None,
                            'If input_type is `image_tensor`, this can explicitly set '
                            'the shape of this input tensor to a fixed size. The '
                            'dimensions are to be provided as a comma-separated list '
                            'of integers. A value of -1 can be used for unknown '
                            'dimensions. If not specified, for an `image_tensor, the '
                            'default shape will be partially specified as '
                            '`[None, None, None, 3]`.')
        flags.DEFINE_string('pipeline_config_path', config_path,  # config路径
                            'Path to a pipeline_pb2.TrainEvalPipelineConfig config '
                            'file.')
        flags.DEFINE_string('trained_checkpoint_prefix', checkpoint_prefix,  # /model.ckpt-86362的路径
                            'Path to trained checkpoint, typically of the form '
                            'path/to/model.ckpt')
        flags.DEFINE_string('output_directory', output_directory, 'Path to write outputs.')  # 输出路径
        flags.DEFINE_string('config_override', '',
                            'pipeline_pb2.TrainEvalPipelineConfig '
                            'text proto to override pipeline_config_path.')
        flags.DEFINE_boolean('write_inference_graph', False,
                             'If true, writes inference graph to disk.')
        tf.app.flags.mark_flag_as_required('pipeline_config_path')
        tf.app.flags.mark_flag_as_required('trained_checkpoint_prefix')
        tf.app.flags.mark_flag_as_required('output_directory')
        FLAGS = flags.FLAGS

        def maain():
            pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
            with tf.gfile.GFile(FLAGS.pipeline_config_path, 'r') as f:
                text_format.Merge(f.read(), pipeline_config)
            text_format.Merge(FLAGS.config_override, pipeline_config)
            if FLAGS.input_shape:
                input_shape = [
                    int(dim) if dim != '-1' else None
                    for dim in FLAGS.input_shape.split(',')
                ]
            else:
                input_shape = None
            exporter.export_inference_graph(
                FLAGS.input_type, pipeline_config, FLAGS.trained_checkpoint_prefix,
                FLAGS.output_directory, input_shape=input_shape,
                write_inference_graph=FLAGS.write_inference_graph)

        maain()



##-----以下为Pre_Work二级窗口的class-----##
class Ui_Pre_Work_Form(QWidget, Ui_Pre_Work_Form):   #第一个Ui_Pre_Work_Form名称可自定义，全篇统一即可；第二个Ui_Pre_Work_Form确定源于re_Work的class名
    def __init__(self, parent=None):  #parent不知用法，删除会报错
        super(Ui_Pre_Work_Form, self).__init__(parent)
        self.setupUi(self)

    ##-----以下为pushButton_getxmlpath功能，确定xml的文件夹路径-----##
    def get_xml_path(self):
        xml_path = QFileDialog.getExistingDirectory(self,   #将选取的文件夹路径存入xml_path
                                                       "打开存在xml的路径",   #弹窗窗口标题为“打开存在xml的路径”
                                                       "",   #弹窗的起始路径
                                                       #" *.xml;;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        print(xml_path)   #打印xml路径方面调试
        x = self.lineEdit_xmlpath
        x.setText(xml_path)   #将路径显示在lineEdit_xmlpath中
        # 以下2行利用qlabel显示图片
        # png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        # self.label.setPixmap(png)
    ##-----以上为pushButton_getxmlpath功能，确定xml的文件夹路径-----##

    ##-----以下为pushButton_getcsvpath功能，确定csv的文件夹路径-----##
    def get_csv_path(self):
        csv_path = QFileDialog.getExistingDirectory(self,   #将选取的文件夹路径存入csv_path
                                                       "打开保存csv的路径",   #弹窗窗口标题为“打开保存csv的路径”
                                                       "",   #弹窗的起始路径
                                                       #" *.xml;;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        print(csv_path)   #打印csv_path路径方便调试
        c = self.lineEdit_csvpath
        c.setText(csv_path)   #将路径显示在lineEdit_csvpath中
        # print(self.lineEdit_csvpath.setText())
        # 一下2行利用qlabel显示图片
        # png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
    ##-----以上为pushButton_getcsvpath功能，确定csv的文件夹路径-----##

    ##-----以下为pushButton_xml2csv功能，将.xml转为.csv-----##
    def xml_to_csv(self):
        # xml_path = os.path.abspath('./xml')   #可为固定路径，当前目录下的名为xml文件夹
        # csv_path = os.path.abspath('../csv')   #可为固定路径，上一级目录下的名为csv文件夹
        xml_path = self.lineEdit_xmlpath.text()  # 读取lineEdit_xmlpath的内容给xml_path
        csv_path = self.lineEdit_csvpath.text()  # 读取lineEdit_csvpath的内容给csv_path
        os.chdir(csv_path)   #设置当前工作目录为csv_path

        def xml_to_csv(self):   #原始公共“xml_to_csv.py”的函数，执行xml转csv的逻辑代码
            xml_list = []
            for xml_file in glob.glob(xml_path + '/*.xml'):   #选取xml_path目录下的.xml结尾文件
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for member in root.findall('object'):
                    value = (root.find('filename').text,
                             int(root.find('size')[0].text),
                             int(root.find('size')[1].text),
                             member[0].text,
                             int(member[4][0].text),
                             int(member[4][1].text),
                             int(member[4][2].text),
                             int(member[4][3].text)
                             )
                    xml_list.append(value)
            column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
            xml_df = pd.DataFrame(xml_list, columns=column_name)
            return xml_df

        def main():   #原始公共“xml_to_csv.py”的函数，调用并执行xml转csv的逻辑代码的代码
            xml_df = xml_to_csv(xml_path)
            xml_df.to_csv('The_csv.csv', index=None)
            print('Successfully converted xml to csv.')

        main()   #调用上面def main（）
    ##-----以上为pushButton_xml2csv功能，将.xml转为.csv-----##

    ##-----以下为pushButton_getcsvpath_2功能，确定.csv的文件路径-----##
    def get_csv_path2(self):
        csv_path2, filetype  = QFileDialog.getOpenFileName(self,   #将选取的文件夹路径存入csv_path2
                                                       "打开存在的csv",   #弹窗窗口标题为“打开路径”
                                                       "",   #弹窗的起始路径
                                                       " *.csv"#;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        print(csv_path2)   #打印csv_path2路径方面调试
        cp2 = self.lineEdit_csvpath_2
        cp2.setText(csv_path2)   #将路径显示在lineEdit_csvpath_2中
        # 一下2行利用qlabel显示图片
        # png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        # self.label.setPixmap(png)
    ##-----以上为pushButton_getcsvpath_2功能，确定.csv的文件路径-----##

    ##-----以下为pushButton_getrecpath功能，确定输出REC文件的文件路径-----##
    def get_image_path(self):
        image_path  = QFileDialog.getExistingDirectory(self,   #将选取的文件夹路径存入image_path
                                                       "打开存在图片样本的目录",   #弹窗窗口标题为“打开路径”
                                                       "",   #弹窗的起始路径
                                                       #" *.csv"#;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        print(image_path)   #打印csv_path2路径方面调试
        cp2 = self.lineEdit_imagepath
        cp2.setText(image_path)   #将路径显示在lineEdit_csvpath_2中
        # 一下2行利用qlabel显示图片
        # png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        # self.label.setPixmap(png)
    ##-----以上为pushButton_getcsvpath_2功能，确定.csv的文件路径-----##

    ##-----以下为pushButton_getrecpath功能，确定输出REC文件的文件路径-----##
    def get_rec_path(self):
        rec_path = QFileDialog.getExistingDirectory(self,   #将选取的文件夹路径存入rec_path
                                                       "打开保存rec的路径",   #弹窗窗口标题为“打开路径”
                                                       "",   #弹窗的起始路径
                                                       #" *.xml;;*.png;;*.jpeg;;*.bmp;;All Files (*)"   #文件类型，注意用双分号间隔
                                                        )
        rec_path_final = rec_path + '/The_TFrecord.record'
        print(rec_path_final)   #打印rec_path路径方面调试
        r = self.lineEdit_recpath
        r.setText(rec_path_final)   #将路径显示在lineEdit_recpath中
        # 一下2行利用qlabel显示图片
        # png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        # self.label.setPixmap(png)
    ##-----以上为pushButton_getrecpath功能，确定输出REC文件的文件路径-----##

    ##-----以下为pushButton_csv2rec功能，将csv转为rec-----##
    def csv_to_rec(self):

        csv_input = self.lineEdit_csvpath_2.text()
        image_dir = self.lineEdit_imagepath.text()
        output_path = self.lineEdit_recpath.text()

        flags = tf.app.flags
        flags.DEFINE_string('csv_input', csv_input, 'Path to the CSV input')
        flags.DEFINE_string('output_path', output_path, 'Path to output TFRecord')
        flags.DEFINE_string('image_dir', image_dir, 'Path to images')
        FLAGS = flags.FLAGS
###---------------------------------------------------------------------------------------------------label需要改动
        # TO-DO replace this with label map
        def class_text_to_int(row_label):
            if row_label == 'Hole':
                return 1
            elif row_label == 'Crack':
                return 2
            else:
                return None

        def split(df, group):
            data = namedtuple('data', ['filename', 'object'])
            gb = df.groupby(group)
            return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

        def create_tf_example(group, path):
            with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
                encoded_jpg = fid.read()
            encoded_jpg_io = io.BytesIO(encoded_jpg)
            image = Image.open(encoded_jpg_io)
            width, height = image.size

            filename = group.filename.encode('utf8')
            image_format = b'jpg'
            xmins = []
            xmaxs = []
            ymins = []
            ymaxs = []
            classes_text = []
            classes = []

            for index, row in group.object.iterrows():
                xmins.append(row['xmin'] / width)
                xmaxs.append(row['xmax'] / width)
                ymins.append(row['ymin'] / height)
                ymaxs.append(row['ymax'] / height)
                classes_text.append(row['class'].encode('utf8'))
                classes.append(class_text_to_int(row['class']))

            tf_example = tf.train.Example(features=tf.train.Features(feature={
                'image/height': dataset_util.int64_feature(height),
                'image/width': dataset_util.int64_feature(width),
                'image/filename': dataset_util.bytes_feature(filename),
                'image/source_id': dataset_util.bytes_feature(filename),
                'image/encoded': dataset_util.bytes_feature(encoded_jpg),
                'image/format': dataset_util.bytes_feature(image_format),
                'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
                'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
                'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
                'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
                'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
                'image/object/class/label': dataset_util.int64_list_feature(classes),
            }))
            return tf_example

        def main():
            writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
            path = os.path.join(FLAGS.image_dir)
            examples = pd.read_csv(FLAGS.csv_input)
            grouped = split(examples, 'filename')
            for group in grouped:
                tf_example = create_tf_example(group, path)
                writer.write(tf_example.SerializeToString())

            writer.close()
            output_path = os.path.join(os.getcwd(), FLAGS.output_path)
            print('Successfully created the TFRecords: {}'.format(output_path))

        main()


    ##-----以上为pushButton_csv2rec功能，将csv转为rec-----##
##-----以上为Pre_Work二级窗口的class-----##
class_texts = {}
total = 3
texts = 'hole,crack,past'
texts = texts.split(',')
for i in range(total):
    class_texts.setdefault(texts[i], i+1)

#使用的时候直接用：
class_texts.get(row_label, None)