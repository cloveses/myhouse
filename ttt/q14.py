# [['songer',[80,80,80,80,80,80,80,80,80,80],score],]

def judge_singer():
    name = input("歌手姓名:")
    scores = []
    for i in range(10):
        score = int(input("输入 %d 号评委评分：" % i+1))
        scores.append(score)
    score = (sum(scores) - max(scores) - min(scores)) / (len(scores) - 2)
    return [name,scores,score]

def main():
    datas = []
    while True:
        q = input('继续输入？（n退出）：')
        if q == n:
            break
        data = judge_singer()
        datas.append(data)
    datas.sort(key=lambda d:d[-1]) # 依据得分排序

    # 输出排序后的评分数据
    for data in datas:
        print("歌手：",data[0],"得分：",data[-1])

    with open('result.txt', 'w') as f:
        for data in datas:
            f.write()

    # 对评委公平性评判
    judges = [0,] * len(datas[0][1])
    for data in datas:
        judges = [j + d -data[-1] for j,d in zip(judges,data[1])]

    judges = [abs(j) for j in judges]
    minn = min(judges)
    print("最公平：%d号" % judges.index(minn))
    maxx = max(judges)
    print("最不公平：%d号" % judges.index(maxx))

if __name__ == '__main__':
    main()


