# 1
datas = [1,3,4,5,6,8,6,6,4,3,2,4,5,9,0,1,3,5,6,8,4,3,1]
res = {1:0,5:0,10:0}
for data in datas:
    if data in res:
        res[data] += 1
for k,v in res.items():
    print(k,v)

#2
totals = int(input('Students amount:'))
sum = 0
for i in range(totals):
    sum += float(input('Please a stud\'s score:'))

print('{:.2f}'.format(sum/totals))

#3


digits = input('Please input some int:')
digits = digits.split(' ')
digits = [int(d) for d in digits if d.isdigit()]
digits.sort()
print(digits[-1] - digits[0])

#4 
sum = 0
b = 2
a = 1
for i in range(20):
    sum += b / a
    b = a + b
    a += 1
print(sum)

#5
astr = input('String:')
res = {'lower':0, 'upper':0, 'digit':0, 'other':0}
for c in astr:
    if 'a' <= c <= 'z':
        res['lower'] += 1
    elif 'A' <= c <= 'Z':
        res['upper'] += 1
    elif '0' <= c <= '9':
        res['digit'] += 1
    else:
        res['other'] += 1
for k,v in res.items():
    print(k,v)

