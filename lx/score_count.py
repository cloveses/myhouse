import fileinput

def funtion1(filename):
    for index,line in enumerate(fileinput.input(filename)):
        if index:
            data = line.strip().split(',')
            scores = [float(data[1]),float(data[2])]
            print('学号：',data[0],'平均分：',int(sum(scores) / len(scores)))


def calAvg(subject,filename='scores.txt'):
    scores = []
    seq = -1
    for index,line in enumerate(fileinput.input(filename)):
        if index:
            data = line.strip().split(',')
            scores.append(float(data[seq]))
        else:
            seq = line.split(',').index(subject)
    return sum(scores) / len(scores)

if __name__ == '__main__':
    funtion1('scores.txt')
    print(calAvg('math'))