distance = input('Please input distance:')
distance = int(distance)
if distance <= 3:
    print('fee:',10)
elif 3 < distance <= 20:
    print('fee:',10 + (distance - 3) * 3)
else:
    print('fee:',10 + (distance - 3) * 3 + (distance - 20) * 0.6)