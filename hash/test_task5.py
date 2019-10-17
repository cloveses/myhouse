from task5 import HashTable

h = HashTable(3)
for i in range(6):
    h[str(i)] = i
for i in range(6):
    print(h[str(i)])