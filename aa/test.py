res = {'a':0,'b':0,'c':0,'d':0}
for i in range(10):
....score = float(input('请输入同学成绩:'))
....if score < 60:
........res['a'] += 1
....elif 60 <= score < 70:
........res['b'] += 1
....elif 70 <= score < 85:
........res['c'] += 1
....elif 85 <= score <=100:
........res['d'] += 1

print('不及格{}人'.format(res['a']))
print('及格{}人'.format(res['b']))
print('良好{}人'.format(res['c']))
print('优秀{}人'.format(res['d']))
