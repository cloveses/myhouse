from task3 import HashTable

def mytest2():
    hashtable = HashTable(3)
    mystrs = ('akdk', 'kdhhgk','kdjih8e','jfuduhd','duhjdffl', )
    for i,mystr in enumerate(mystrs):
        print(hashtable.hash(mystr))
        hashtable[mystr] = i
        print(hashtable.table, hashtable.count)
    for mystr in mystrs:
        print(mystr, hashtable[mystr])
    print(hashtable.statistics())

if __name__ == '__main__':
    mytest2()