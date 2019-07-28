import os
import sys
import pwd
import grp
import time
import stat

def get_fileinfo(file):
    infos = []
    st = os.stat(file)
    infos.append(stat.filemode(st.st_mode))
    infos.append(str(st.st_nlink))
    infos.append(pwd.getpwuid(st.st_uid).pw_name)
    infos.append(grp.getgrgid(st.st_gid).gr_name)
    infos.append(str(st.st_size))
    infos.append(time.asctime(time.localtime(st.st_mtime)))
    infos.append(file)
    return infos

def main(argv):
    if len(argv) > 1:
        options = ''.join(argv[1:])
    else:
        options =''
    files = os.listdir()

    # print(options)

    if 'a' not in options:
        files = [f for f in files if not f.startswith('.')]

    file_infos = [[f,] for f in files]

    if 'l' in options:
        file_infos = [get_fileinfo(f[0]) for f in file_infos]

    if 'i' in options:
        for i in range(len(file_infos)):
            file_infos[i].insert(0,str(os.stat(file_infos[i][-1]).st_ino))


    for file_info in file_infos:
        print('\t'.join(file_info))


if __name__ == '__main__':
    main(sys.argv)