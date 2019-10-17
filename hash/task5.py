class HashTable:
    def __init__(self, table_capacity=163, hash_base=31415):
        self.table_capacity = table_capacity
        self.hash_base = hash_base
        self.count = 0
        self.table = [None] * table_capacity
  
    def __getitem__(self, key):
        pass

    def __setitem__(self, key, item):
        pass

    def __contains__(self, key):
        pass
    
    def hash(self, key):
        if not isinstance(key, str):
            raise TypeError
        value = 0
        for i in range(len(key)):
            value = (value*self.hash_base + ord(key[i])) % self.table_capacity
        return value

import time

def load_dictionary(hash_table, filename, time_limit=None):
    start = time.time()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip()
            hash_table[word] = 1
            if time_limit:
                duration = (time.time() - start)
                if duration >= time_limit:
                    raise TimeoutError('Time out!')
    return (time.time() - start)


def load_dictionary_statistics(hash_base, table_size, filename, max_time):
    hashtable = HashTable(table_capacity=table_size, hash_base=hash_base)
    try:
        duration = load_dictionary(hashtable, filename, max_time)
        res = [hashtable.count, duration]
        res.extend(hashtable.statistics())
        return tuple(res)
    except TimeoutError:
        res = [hashtable.count, None]
        res.extend(hashtable.statistics())
        return tuple(res)

def table_load_dictionary_statistics(max_time):
    files = ('english_small.txt', 'english_large.txt', 'french.txt')
    hash_bases = (1, 27183, 250726)
    table_sizes = (250727, 402221, 1000081)
    res = []
    for file in files:
        for hash_base in hash_bases:
            for table_size in table_sizes:
                data = load_dictionary_statistics(hash_base, table_size, file, max_time)
                datas = [file, table_size, hash_base]
                datas.extend(data)
                datas = [str(d) for d in datas]
                res.append(datas)
                print(datas)
    with open('output_task4.csv', 'w') as f:
        for r in res:
            line = ','.join(r)
            f.write(line)
            f.write('\n')

if __name__ == '__main__':
    table_load_dictionary_statistics(120)
