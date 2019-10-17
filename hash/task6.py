import re

class HashTable:
    def __init__(self, table_capacity=52361, hash_base=31415):
        self.table_capacity = table_capacity
        self.hash_base = hash_base
        self.count = 0
        self.table = [None] * table_capacity
  
    def __getitem__(self, key):
        di = 0
        while True:
            key_hash = (self.hash(key) + di) % self.table_capacity
            # key_hash超出表的范围或对应位置为空
            if key_hash > self.table_capacity or not self.table[key_hash]:
                raise KeyError
            # hash位置不为空，key值相等代表查找到
            elif self.table[key_hash] and self.table[key_hash][0] == key:
                return self.table[key_hash][1]
            di += 1

    def __setitem__(self, key, item):
        # 超过表长的一半则扩充表
        if self.count >= self.table_capacity / 2:
            self.rehash()
        di = 0
        while True:
            # 循环计算hash值
            key_hash = (self.hash(key) + di) % self.table_capacity
            # 查找到可以存放的位置
            if not self.table[key_hash]:
                self.table[key_hash] = (key, item)
                self.count += 1
                break
            elif self.table[key_hash] and key == self.table[key_hash][0]:
                self.table[key_hash] = (key, self.table[key_hash][1] + item)
                raise KeyError
            di += 1
        # raise NotImplementedError

    def __contains__(self, key):
        di = 0
        while True:
            key_hash = (self.hash(key) + di) % self.table_capacity
            if self.table[key_hash] and self.table[key_hash][0] == key:
                return True
            elif key_hash > self.table_capacity:
                return False
            elif not self.table[key_hash]:
                return False
            di += 1
        return False
        # raise NotImplementedError

    def hash(self, key):
        # key不是字符串，则抛出异常
        if not isinstance(key, str):
            raise TypeError
        value = 0
        # 计算hash值
        for i in range(len(key)):
            value = (value*self.hash_base + ord(key[i])) % self.table_capacity
        return value

    def rehash(self):
        # print('rehash start...')
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
        # print('cap:', self.table_capacity)
        old_table = self.table[:]
        self.table = [None] * self.table_capacity
        self.count = 0
        for k,v in [o for o in old_table if o]:
            self.__setitem__(k, v)

        # raise NotImplementedError

class Freq:

    def __init__(self):
        self.maxum = 0
        self.hash_table = HashTable()

    def add_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                words = re.split(r'[^a-zA-Z\-]+',line.strip().lower())
                for word in words:
                    w = word.strip()
                    if w:
                        try:
                            self.hash_table[w] = 1
                        except KeyError:
                            times = self.hash_table[w]
                            if times > self.maxum:
                                self.maxum = times

    def rarity(self, word):
        word = word.lower()
        if not word in self.hash_table:
            return 3
        times = self.hash_table[word]
        if times >= self.maxum / 100:
            return 0
        elif times <= self.maxum / 1000:
            return 2
        else:
            return 1