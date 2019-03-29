# 1

n = input('Int:')
m = n[::-1]
print('m=%d' % int(m))

bigs = [1,3,5,7,8,10,12]
smalls = [4,6,9,11]
y,m=int(input('Year:')),int(input('Month:'))
if m in bigs:
    print('Year:%d Month:%d Days:%d' % (y,m,31))
elif m in smalls:
    print('Year:%d Month:%d Days:%d' % (y,m,30))
else:
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        print('Year:%d Month:%d Days:%d' % (y,m,29))
    else:
        print('Year:%d Month:%d Days:%d' % (y,m,28))

code = input('Code:')
times = float(input('time:'))
sum = 84 * times
if times < 60:
    sum = sum - 700 if sum - 700 > 0 else 0
elif times > 120:
    sum += (times - 120) * 0.15
print('Code:%s salary:%f' % (code, sum))