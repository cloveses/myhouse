import os
import tarfile
import fileinput

def update_txt_file(names,filename='records.txt'):
    ## 更新保存已处理压缩文件的文本文件
    with open(filename, 'w+') as file:
        for name in names:
            file.write(name)
            file.write('\n')

def filter_files(files,filename='records.txt'):
    ## 根据提供的文件名，依据文本文件，过滤掉已处理过的压缩文件
    datas = []
    if os.path.exists(filename):
        ## 读取文本文件
        for line in fileinput.input(filename):
            datas.append(line.strip())
    if not datas:
        return files

    res = []
    for file in files:
        if file not in files:
            res.append(file)
    return res


def edit_file(filename):
    # 打工压缩文件
    tar = tarfile.open(filename)
    ## 抽取所需文件
    tar.extract('bpa_online.DAT')
    tar.extract('bpa_online.SWI')

    ## 重新压缩文件
    tar = tarfile.open(filename,'w:gz')
    tar.add('bpa_online.DAT')
    tar.add('bpa_online.SWI')
    ## 移除抽取的文件
    os.remove('bpa_online.DAT')
    os.remove('bpa_online.SWI')

def main():
    files = os.listdir('.')
    files = [f for f in files if f.endswith('.tar.gz')]
    files = filter_files(files)
    for file in files:
        edit_file(file)
    update_txt_file(files)

if __name__ == '__main__':
    main()
