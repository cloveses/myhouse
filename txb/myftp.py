import os
from ftplib import FTP

class MyFtp:
    def __init__(self, server, user, passwd):
        self.server = server
        self.user = user
        self.passwd = passwd
        self.rpath_depth = 0
        self.ftp = None

    # 连接服务器函数
    def connect(self):
        for i in range(2):
            try:
                self.ftp = FTP(host=self.server, user=self.user, passwd=self.passwd)
                if self.ftp:
                    return
            except:
                print('times %d' % (i+1))

    #获取指定路径的所有路径名称列表
    def get_pathes(self,path):
        paths = []
        while True:
            pathlst = os.path.split(path)
            if  not pathlst[0] or not pathlst[-1] or pathlst == '.':
                break
            paths.append(pathlst[-1])
            path = pathlst[0]
        return paths[::-1]


    # 测试路径名是否在服务器返回的路径列表中
    def exists(self,dlst,directory):
        # for d in dlst:
        #     if d.startswith('d') and d.endswith(directory):
        #         return True
        return directory in dlst

    # 进行要上传的FTP服务器目录
    def enter_dir(self, paths, dest_dir):
        # 首先切换到服务器的目标根目录
        res = self.ftp.cwd(dest_dir)
        if not res.startswith('250'):
            print('change directory failed!')
            return
        paths = self.get_pathes(paths)
        # print(paths)
        paths = paths[self.rpath_depth:]
        # 逐级进行目录目录，不存在，则创建
        for path in paths:
            res = self.ftp.nlst()
            print('dirlst:',res)
            if not self.exists(res, path):
                print('create:',path)
                res = self.ftp.mkd(path)
                # if not res.strip():
                #     print('deny!')
                #     return
            res = self.ftp.cwd(path)
            if not res.startswith('250'):
                return
        return True

    # 上传文件函数
    def upload(self, path, dest_dir):
        #测试本地目录是否存在，并转为绝对路径
        if not os.path.exists(path):
            print('directory is not exists!')
            return
        else:
            path = os.path.abspath(path)
        self.rpath_depth = len(self.get_pathes(path)) - 1
        if self.rpath_depth < 0:
            self.rpath_depth = 0
        # 获取本地目录中所有文件
        all_files = os.walk(path)
        #调用函数连接FTP服务器
        self.connect()
        if not self.ftp:
            print('Link error!')
            return
        self.ftp.encoding = 'gbk'
        # 逐目录上传文件
        for root,dirs,files in all_files:
            if files:
                # 进行目标路径
                self.enter_dir(root, dest_dir)
                for f in files:
                    print(root)
                    fp = open(os.path.join(root,f),'rb')
                    res = self.ftp.storbinary('STOR ' + f, fp)
                    if not res.startswith('226'):
                        print('Put file Failed!')
                    fp.close()
        self.ftp.quit()


    def download(self,serverpath, local_path='.\\'):
        self.connect()
        if not self.ftp:
            print('Link error!')
            return
        self.ftp.encoding = 'gbk'
        self.local_root_path = os.path.abspath(local_path)
        self.downloads(serverpath, local_path)

    def downloads(self, rpath, local_path):

        res = self.ftp.cwd(rpath)
        if not res.startswith('250'):
            print('change directory failed!')
            return

        os.chdir(self.local_root_path)

        if not os.path.exists(local_path):
            os.makedirs(local_path)
        os.chdir(local_path)

        datas = []
        self.ftp.retrlines('LIST',lambda s:datas.append(s))

        files = [f.split(' ')[-1] for f in datas if not f.startswith('d')]
        directorys = [f.split(' ')[-1] for f in datas if f.startswith('d')]

        for filename in files:
            with open(filename,'wb') as f:
                self.ftp.retrbinary('RETR ' + filename, f.write)

        for d in directorys:
            next_rpath = rpath + d if rpath == '/' else '/'.join((rpath,d))
            self.downloads(next_rpath, os.path.join(local_path,d))

if __name__ == '__main__':
    ftp = MyFtp('127.0.0.1', 'anonymous', '')
    # ftp.upload('D:\\lx\\qx', '/ass')
    ftp.download('/')