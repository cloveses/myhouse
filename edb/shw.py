import os
import sys
import tarfile
import fileinput
import time

FILE_DEST = 'd:\\temp'  #解压文件目录
TAR_DEST = 'd:\\retar'  #新压缩包目录
SRC_DEST = '.'          #源压缩包目录
DEL_DATE = '2018-12-11' #删除压缩包时间点
TAR_DATE = '2018-12-11' #指定处理压缩包文件时间点
FILES_LIST = ('bpa_online.DAT','bpa_online.SWI')    #要处理压缩包中的文件

def edit_file(filename):
    if not os.path.exists(os.path.join(TAR_DEST,filename)):
        # 打开压缩文件
        tar = tarfile.open(os.path.join(SRC_DEST,filename))
        ## 抽取所需文件
        for file in FILES_LIST:
            tar.extract(file, path=FILE_DEST)

        ## 重新压缩文件
        tar = tarfile.open(os.path.join(TAR_DEST,filename),'w:gz')
        for file in FILES_LIST:
            tar.add(os.path.join(FILE_DEST,file),file)

        ## 改名抽取的文件
        for file in FILES_LIST:
            nfile = ''.join((file[:4],filename[:14],file[-4:]))
            os.rename(os.path.join(FILE_DEST,file),os.path.join(FILE_DEST,nfile))

def deal_files(files):
    dels = []
    deals = []
    del_duration = time.mktime(time.strptime(DEL_DATE,'%Y-%m-%d'))
    deal_duration = time.mktime(time.strptime(TAR_DATE,'%Y-%m-%d'))
    for file in files:
        t = os.path.getmtime(os.path.join(SRC_DEST,file))
        if t < del_duration:
            dels.append(file)
        if t > deal_duration:
            deals.append(file)

    # 处理压缩包文件
    for file in deals:
        edit_file(file)

    # 删除压缩包文件
    for file in dels:
        os.remove(os.path.join(SRC_DEST,file))


def main():
    if not os.path.exists(FILE_DEST):
        os.makedirs(FILE_DEST)
    if not os.path.exists(TAR_DEST):
        os.makedirs(TAR_DEST)
    files = os.listdir(SRC_DEST)
    files = [f for f in files if f.endswith('.tar.gz')]
    deal_files(files)

if __name__ == '__main__':
    main()