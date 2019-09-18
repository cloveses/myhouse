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
        self.p = Process(target=mystart_train, args=())
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