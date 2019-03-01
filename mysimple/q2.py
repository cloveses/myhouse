x = int(input('Please input a integer:'))
datas = []
num = 0
for i in range(1,x):
    if i % 5 == 0:
        datas.append(i)
        num += 1
print('total:', num)
print(datas)