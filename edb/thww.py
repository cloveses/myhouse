import os
import sys
import tarfile
import fileinput

DEST = 'd:\\temp'


def edit_file(filename):
    # 打工压缩文件
    tar = tarfile.open(filename)
    ## 抽取所需文件
    tar.extract('bpa_online.DAT')
    tar.extract('bpa_online.SWI')
    tarfile_name = os.path.join(DEST,os.path.split(filename)[-1])
    ## 重新压缩文件
    tar = tarfile.open(tarfile_name,'w:gz')
    tar.add('bpa_online.DAT')
    tar.add('bpa_online.SWI')
    ## 移除抽取的文件
    os.remove('bpa_online.DAT')
    os.remove('bpa_online.SWI')
    os.remove(filename)

def main():
    if not os.path.exists(DEST):
        os.makedirs(DEST)
    args = sys.argv
    path = '.'
    if len(args) == 2:
        path = args[1]
    files = os.listdir(path)
    if path == '.':
        path = os.path.abspath(path)
    files = [os.path.join(path,f) for f in files if f.endswith('.tar.gz')]
    for file in files:
        edit_file(file)

if __name__ == '__main__':
    main()
