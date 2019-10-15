from task1 import HashTable

def mytest():
    hashtable = HashTable(7)
    mystrs = ('akdk', 'kdhhgk','kdjih8e','jfuduhd','duhjdffl')
    for i,mystr in enumerate(mystrs):
        print(hashtable.hash(mystr))
        hashtable[mystr] = i
        print(hashtable.table, hashtable.count)
    for mystr in mystrs:
        print(hashtable[mystr])

def mytest2():
    hashtable = HashTable(3)
    mystrs = ('akdk', 'kdhhgk','kdjih8e','jfuduhd','duhjdffl', )
    for i,mystr in enumerate(mystrs):
        print(hashtable.hash(mystr))
        hashtable[mystr] = i
        print(hashtable.table, hashtable.count)
    for mystr in mystrs:
        print(mystr, hashtable[mystr])

if __name__ == '__main__':
    mytest2()