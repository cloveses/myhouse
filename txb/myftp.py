import os
from ftplib import FTP

class MyFtp:
    def __init__(self, server, user, passwd):
        self.server = server
        self.user = user
        self.passwd = passwd
        self.ftp = None
        self.connect()

    def connect(self):
        for i in range(2):
            try:
                self.ftp = FTP(host=self.server, user=self.user, passwd=self.passwd)
                if self.ftp:
                    return
            except:
                print('times %d' % (i+1))

    def get_pathes(self,path):
        paths = []
        while True:
            pathlst = os.path.split(path)
            if  not pathlst[0] or not pathlst[-1] or pathlst == '.':
                paths.append(pathlst[-1])
                break
            paths.append(pathlst[-1])
            path = pathlst[0]
        return paths[::-1]

    def exists(self,dlst,directory):
        for d in dlst:
            if d.startswith('d') and d.endswith(directory):
                return True


    def enter_dir(self,paths):
        res = self.ftp.cwd('/')
        if not res.startswith('250'):
            print('change directory failed!')
            return
        paths = self.get_pathes(paths)
        print(paths)
        for path in paths:
            res = self.ftp.nlst()
            if not self.exists(res, path):
                res = self.ftp.mkd(path)
                # if not res.strip():
                #     print('deny!')
                #     return
            res = self.ftp.cwd(path)
            if not res.startswith('250'):
                return
        return True

    def upload(self, path):
        if not self.ftp:
            print('Link error!')
            return
        if not os.path.exists(path):
            print('directory is not exists!')
            return
        all_files = os.walk(path)
        for root,dirs,files in all_files:
            if files:
                self.enter_dir(root)
                for f in files:
                    print(root)
                    fp = open(os.path.join(root,f),'rb')
                    res = self.ftp.storbinary('STOR ' + f, fp)
                    if not res.startswith('226'):
                        print('Put file Failed!')
                    fp.close()

if __name__ == '__main__':
    ftp = MyFtp('127.0.0.1', 'anonymous', '')
    ftp.upload('aa')