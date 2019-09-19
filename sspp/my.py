import re

texts = []

def clear(word):
    if re.match(r'["\']\S+',word):
        word = word[1:]
    if re.match(r'\S+["\']$',word):
        word = word[:-1]
    s = ''
    for w in word:
        if w.isalpha():
            s += w
    return s

with open('THE TRAGEDY OF ROMEO AND JULIET.txt', 'r') as f:
    for line in f.readlines():
        words = line.strip().split()
        words = [w.lower() for w in words if w]
        words = [clear(w) for w in words]
        texts.extend(words)


print(texts[:10])
datas = {}
for text in texts:
    if text in datas:
        datas[text] += 1
    else:
        datas[text] = 1
datas = [(v,k) for k,v in datas.items()]
datas.sort(key=lambda x:x[0], reverse=True)
for data in datas[:30]:
    print(data, end=',')
