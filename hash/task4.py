class HashTable:
    def __init__(self, table_capacity=163, hash_base=31415):
        self.table_capacity = table_capacity
        self.hash_base = hash_base
        self.count = 0
        self.table = [None] * table_capacity

        self.collisions = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash_count = 0
  
    def __getitem__(self, key):
        di = 0
        while True:
            qdi = ((-1) ** ((di + 1) % 2)) * (((di + 1) // 2) ** 2)
            key_hash = (self.hash(key) + qdi) % self.table_capacity
            if key_hash > self.table_capacity or not self.table[key_hash]:
                raise KeyError
            elif self.table[key_hash] and self.table[key_hash][0] == key:
                return self.table[key_hash][1]
            di += 1

    def __setitem__(self, key, item):
        di = 0
        while True:
            qdi = ((-1) ** ((di + 1) % 2)) * (((di + 1) // 2) ** 2)
            key_hash = (self.hash(key) + qdi) % self.table_capacity
            if key_hash > (self.table_capacity - 1) or self.count >= self.table_capacity:
                self.rehash()
                self.rehash_count += 1
                di = 0
                continue
            elif not self.table[key_hash]:
                self.table[key_hash] = (key, item)
                self.count += 1
                self.probe_total += di
                if di > self.probe_max:
                    self.probe_max = di
                break
            elif self.table[key_hash] and key == self.table[key_hash][0]:
                self.table[key_hash][1] = item
                # raise KeyError
            elif self.table[key_hash]:
                self.collisions += 1
            di += 1

    def __contains__(self, key):
        di = 0
        while True:
            qdi = ((-1) ** ((di + 1) % 2)) * (((di + 1) // 2) ** 2)
            key_hash = (self.hash(key) + qdi) % self.table_capacity
            if self.table[key_hash] and self.table[key_hash][0] == key:
                return True
            elif key_hash > self.table_capacity:
                return False
            elif not self.table[key_hash]:
                return False
            di += 1
        return False

    def hash(self, key):
        if not isinstance(key, str):
            raise TypeError
        value = 0
        for i in range(len(key)):
            value = (value*self.hash_base + ord(key[i])) % self.table_capacity
        return value

    def rehash(self):
        primes = [ 3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761,
            919, 1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591,
            17519, 21023, 25229, 30313, 36353, 43627, 52361, 62851, 75521, 90523, 108631, 130363, 156437,
            187751, 225307, 270371, 324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263,
            1674319, 2009191, 2411033, 2893249, 3471899, 4166287, 4999559, 5999471, 7199369]
        for prime in primes:
            if (2 * self.table_capacity) <= prime:
                self.table_capacity = prime
                break
        else:
            raise ValueError
        old_table = self.table[:]
        self.table = [None] * self.table_capacity
        self.count = 0
        for k,v in [o for o in old_table if o]:
            self.__setitem__(k, v)

    def statistics(self):
        return (self.collisions,self.probe_total, self.probe_max, self.rehash_count)

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
    table_load_dictionary_statistics(60)
