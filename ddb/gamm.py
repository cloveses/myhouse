import time
import random
import math
import fileinput
import os

FILENAME = 'high_score.txt'

def out():
    if os.path.exists(FILENAME):
        datas = []
        for line in fileinput.input(FILENAME):
            datas.append(line.strip().split('\t'))
        datas.sort(key=lambda d:d[1])
        for data in datas:
            print('\t'.join(data),'\n')

def display():
    if os.path.exists(FILENAME):
        for line in fileinput.input(FILENAME):
            print(line.split('\t')[0])

def update_file(name,duration,fault):
    datas = dict()
    if os.path.exists(FILENAME):
        for line in fileinput.input(FILENAME):
            line = line.strip()
            if line:
                n,t,f = line.split('\t')
                datas[n] = (float(t),int(f))

    if name in datas:
        if fault < datas[name][1]:
            datas[name] = (duration,fault)
    else:
        datas[name] = (duration,fault)

    with open(FILENAME,'w') as file:
        for k,(t,f) in datas.items():
            file.write('\t'.join((k,str(t),str(f))))
            file.write('\n')

def start():
    name = input('Please input your name:')
    if name:
        start = time.time()
        fault = 0
        for i in range(5):
            a,b = random.randint(0,50),random.randint(0,50)
            print()
            print(a,'+',b,'=',end='')
            result = input()
            while True:
                if result and result.isdigit():
                    if a + b != int(result):
                        fault += 1
                    break
                else:
                    input('Please a integer:')
        end = time.time()
        duration = end - start
        update_file(name,duration,fault)


def mstart():
    print()
    Auswahl=input("a) High-Score\nb)Neuer Name\nc)Bereits existierender Name\n\nbitte wahlen sie:")
    if Auswahl == 'a':
        out()
    elif Auswahl == 'b':
        start()
    elif Auswahl == 'c':
        display()
    elif Auswahl == 'n':
        return 'exit'
    else:
        print('Please input: a,b or c!')

def main():
    while True:
        res = mstart()
        if res == 'exit':
            break

if __name__ == '__main__':
    main()
