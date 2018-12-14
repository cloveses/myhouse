import os
import sys
import tarfile
import fileinput
import time

FILE_DEST = 'd:\\temp'  #解压文件目录
TAR_DEST = 'd:\\temp'  #新压缩包目录
SRC_DEST = '.'          #源压缩包目录
DEL_DATE = '2018-12-11' #删除压缩包时间点
TAR_DATE = '2018-12-11' #指定处理压缩包文件时间点
FILES_LIST = ('bpa_online.DAT','bpa_online.SWI')    #要处理压缩包中的文件

def edit_file(src_dest, file_dest, tar_dest,filename):
    if not os.path.exists(os.path.join(tar_dest,filename)):
        # 打开压缩文件
        tar = tarfile.open(os.path.join(src_dest,filename))
        ## 抽取所需文件
        for file in FILES_LIST:
            tar.extract(file, path=file_dest)

        new_name = ''.join(('bpa_',filename[:14]))
        ## 改名抽取的文件
        for file in FILES_LIST:
            nfile = ''.join((new_name,file[-4:]))
            # print(nfile)
            if os.path.exists(os.path.join(file_dest,nfile)):
                os.remove(os.path.join(file_dest,nfile))
            os.rename(os.path.join(file_dest,file),os.path.join(file_dest,nfile))

        new_tar_file = ''.join((new_name,filename[-7:]))
        ## 重新压缩文件
        tar = tarfile.open(os.path.join(TAR_DEST,new_tar_file),'w:gz')
        for file in FILES_LIST:
            name = ''.join((new_name,file[-4:]))
            tar.add(os.path.join(file_dest,name),name)

def deal_files(src_dest, file_dest, tar_dest):
    files = os.listdir(src_dest)
    files = [f for f in files if f.endswith('.tar.gz')]

    dels = []
    deals = []
    del_duration = time.mktime(time.strptime(DEL_DATE,'%Y-%m-%d'))
    deal_duration = time.mktime(time.strptime(TAR_DATE,'%Y-%m-%d'))
    for file in files:
        t = os.path.getmtime(os.path.join(src_dest,file))
        if t < del_duration:
            dels.append(file)
        if t > deal_duration:
            deals.append(file)

    # 处理压缩包文件
    for file in deals:
        edit_file(src_dest, file_dest, tar_dest, file)

    # 删除压缩包文件
    for file in dels:
        os.remove(os.path.join(src_dest,file))


def main():
    if not os.path.exists(FILE_DEST):
        os.makedirs(FILE_DEST)
    if not os.path.exists(TAR_DEST):
        os.makedirs(TAR_DEST)
    deal_files(SRC_DEST,FILE_DEST,TAR_DEST)

if __name__ == '__main__':
    main()