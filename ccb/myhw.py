# -*- coding=utf-8 -*-

import os,os.path
import sys
import time

def out(dir,files):
    print('Directory','<%s>' % dir)
    datas = []
    for file in files:
        path = os.path.join(dir,file)
        size = os.path.getsize(path)
        dt = os.path.getmtime(path)
        name = file
        datas.append((size,dt,name))
    datas.sort(key=lambda f:f[0])
    for s,d,n in datas:
        print('\t', end=' ')
        print(s,end=' ')
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(d)),end=' ')
        print(n)
    print()

def get_files(directory):
    abs_dir = os.path.abspath(directory)
    file_dirs = os.listdir(abs_dir)
    files = [f for f in file_dirs if os.path.isfile(os.path.join(abs_dir,f))]
    out(abs_dir,files)
    dirs = [d for d in file_dirs if os.path.isdir(os.path.join(abs_dir,d))]
    if dirs:
        for dir in dirs:
            get_files(os.path.join(abs_dir,dir))

def main():
    args = sys.argv
    if len(args) == 2:
        get_files(args[1])
    else:
        print('Please add a directory for listing!')

if __name__ == '__main__':
    main()

