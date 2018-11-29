import fileinput

def main(filename):
    ret = {}
    for line in fileinput.input(filename):
        if line.startswith('From: ') and '@' in line:
            mail = line.split(' ')[-1].strip()
            if mail in ret:
                ret[mail] += 1
            else:
                ret[mail] = 1
    print(ret)

if __name__ == '__main__':
    main('mbox-short.txt')