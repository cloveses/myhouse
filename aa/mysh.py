import os
import time
import sys

def my_chdir(p):
    if p and os.path.exists(p):
        os.chdir(p)
    else:
        print('no dir or dir is null!')

def my_date():
    t = time.localtime()
    tzone = t.tm_zone
    r = time.asctime(t)
    r = r.split()
    r.insert(-1, tzone)
    return ' '.join(r)

def my_pwd(p='.'):
    return os.path.abspath(p)

def my_exit():
    sys.exit(0)

coms = {'pwd':my_pwd,
    'date':my_date,
    'exit':my_exit}

def main():
    while True:
        com = input('mysh> ')
        com = com.strip()
        if ' ' not in com and com in coms:
            print(coms[com]())
            continue
        if com.startswith('cd '):
            my_chdir(com[3:])
            continue
        if '|' in com:
            os.system(com)

if __name__ == '__main__':
    main()