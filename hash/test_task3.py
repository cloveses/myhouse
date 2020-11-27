from task3 import HashTable

mystrs = ('akdk', 'kdhhgk','kdjih8e','jfuduhd','duhjdffl', )

def mytest2(mystrs=mystrs):
    hashtable = HashTable(3)
    for i,mystr in enumerate(mystrs):
        # print(hashtable.hash(mystr))
        hashtable[mystr] = i
        # print(hashtable.table, hashtable.count)
    # for mystr in mystrs:
    #     print(mystr, hashtable[mystr])
    print(hashtable.statistics())

def test_files(files=('words.txt', 'wordsb.txt', 'wordsc.txt')):
    for file in files:
        words = []
        with open(file, 'r') as f:
            for line in f.readlines():
                if line.strip():
                    words.append(line.strip())
        mytest2(words)

if __name__ == '__main__':
    mytest2()
    test_files()