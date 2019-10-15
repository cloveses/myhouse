class HashTable:
    def __init__(self, table_capacity = 128, hash_base = 31415):
        self.table_capacity = table_capacity
        self.hash_base = hash_base
        self.array = [None] * self.table_capacity
        self.count = 0

    def __setitem__(self, key, value):
        position = self.hash(key)
        for _ in range(self.table_capacity):
            if self.array[position] is None:
                self.array[position] = (key, value)
                self.count += 1
                return
            elif self.array[position][0] == key:
                self.array[position] = (key, value)
                return
            else:
                position = (position + 1) % self.table_capacity

        self.rehash()
        self.__setitem__(key, value)

    def __getitem__(self, key):
        position = self.hash(key)
        for _ in range(self.table_capacity):
            if self.array[position] is None:
                raise KeyError(key)
            elif self.array[position][0] == key:
                return self.array[position][1]
            else:
                position = (position + 1) % self.table_capacity
        raise KeyError(key)

    def __contains__(self, key):
        position = self.hash(key)
        for _ in range(self.table_capacity):
            if (self.array[position] is not None) and (self.array[position][0] == key):
                return True
            else:
                position = (position + 1) % self.table_capacity
        return False

    def hash(self, key):
        value = 0
        for i in range(len(key)):
            value = (value*self.hash_base + ord(key[i])) % self.table_capacity
        return value


"""
    def rehash(self):
        primes = [3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761,
                  919, 1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591,
                  17519, 21023, 25229, 30293, 36353, 43627, 52361, 62851, 75431, 90523, 108631, 130363, 156437,
                  187751, 225307, 270371, 324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263,
                  1674319, 2009191, 2411033, 2893249, 3471899, 4166287, 4999559, 5999471, 7199369]

        old_array = self.array
        found = False
        for i in range(len(primes)):
            if (2 * self.table_capacity) < primes[i]:
                new_size = primes[i]
                found = True
                break
        if not found:
            raise ValueError("No such prime in the list")
        self.array = [None] * new_size
        self.count = 0

        for entry in old_array:
            if entry is not None:
                self.__setitem__(entry[0], entry[1])
"""




h = HashTable(7,3)
print(h.hash('line'))


