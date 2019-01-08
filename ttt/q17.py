import os
import random

def deal_file(name,score):
    filename = 'guess.txt'
    scores = []
    if os.path.exists(filename):
        with open(filename,'r') as f:
            # 把数据整理为[(name,score),...]格式
            datas = f.read().split('\n')
            datas = [d.strip() for d in datas if d.strip()]
            datas = [d.split(',') for d in datas]
            datas = [(d,int(s)) for d,s in datas]
            scores.extend(datas)
            scores.append((name,score))
            scores.sort(key=lambda s:s[1])
            scores = scores[:5]
            print('-----------')
            print('当前最好成绩排名：')
            for index,data in enumerate(scores):
                print(data[0],data[1],index+1)
            print('------------')
    else:
        scores.append((name,score))
        print(name,score,1)
    if scores:
        with open(filename,'w') as f:
            for n,s in scores:
                f.write(n)
                f.write(',')
                f.write(str(s))
                f.write('\n')

def guess(minn=1, maxn=20):
    while True:
        name = input('请输入你名字：')
        if name:
            break
    # 生成随机数
    passwd = random.randint(minn,maxn)
    print('数字范围：',minn,'-',maxn)
    score = 0

    while True:
        g = input('请输入你猜的结果：')
        if not g.isdigit():
            print('请输入一个整数')
            continue
        score += 1
        g = int(g)
        if g > passwd:
            print('大了！')
        elif g < passwd:
            print('小了！')
        else:
            print('恭喜，猜中了！')
            break

    deal_file(name,score)

def main():
    guess()


if __name__ == '__main__':
    main()
