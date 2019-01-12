

class Singer:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores
        self.cacu()

    def cacu(self):
        self.score = (sum(self.scores) - max(self.scores) \
                 - min(self.scores))/ len(self.scores)
        self.deferents = [s - self.score for s in self.scores]

    def myprint(self):
        print('姓名：',self.name,'得分：',self.score)

def get_scores():
    ret = []
    num = 1
    while len(ret) < 10:
        score = input("输入%d号评委评分：" % num)
        if score.isdigit():
            score = int(score)
            if 0 <= score <= 100:
                ret.append(score)
                num += 1
            else:
                print('输入的分数范围为0-100，请重新输入！')
        else:
            print('你输入的不是整数，请重新输入！')
    return ret

def start():
    singers = []
    while True:
        name = input('请输入歌手姓名：')
        if name:
            scores = get_scores()
            singers.append(Singer(name,scores))
        else:
            print('歌手的姓名不能为空！')
        yes = input('是否继续录入(y/n)？')
        if yes.lower() == 'n':
            break
    singers.sort(key=lambda s : s.score)
    scores = [0,] * 10
    for singer in singers:
        singer.myprint()
        scores = [a+b for a,b in zip(scores,singer.deferents)]
    scores = [abs(s) for s in scores]
    print('最公平评委是：',scores.index(min(scores))+1,'号。')
    print('最不公平评委是：',scores.index(max(scores))+1,'号。')

    with open('singer.txt', 'w') as myfile:
        for singer in singers:
            myfile.write('\t'.join([str(s) for s in singer.scores]))
            myfile.write('\t' + str(singer.score) + '\n')

start()