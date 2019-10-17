class Node(object):
    __slots__ = ['left', 'right', 'data', 'key']
 
    def __init__(self, data, left=None, right=None):
        self.key = data[0]
        self.data = data[1]
        self.left = left
        self.right = right
 
    def __str__(self):
        sl = '%s <-' % self.left if self.left else ''
        sr = '-> %s' % self.right if self.right else ''
        return '[%s Node(%s, %s) %s]' % (sl, self.key, self.data, sr)
 
class BinarySearchTree:
    def __init__(self):
        self.root = None
 
    def insert(self, data):
        node, parent = self.search(data[0], True)
        if node:
            raise ValueError('"%s" has been in tree.' % data)
 
        node = Node(data)
        if parent is None:
            self.root = node
        elif data[0] < parent.key:
            parent.left = node
        else:
            parent.right = node 
 
    def search(self, data, retParent=False):
        parent = None
        node = self.root
 
        while node and node.key != data[0]:
            parent = node
            if data[0] < node.key:
                node = node.left
            else:
                node = node.right
 
        return (node, parent) if retParent else node
 
    def delete(self, data):
        self._deleteNode(*self.search(data, True))
 
    def _findBiggest(self, node):
        parent = None
        while node.right:
            parent = node
            node = node.right
        return node, parent
 
    def _deleteNode(self, node, parent):
        if node is None:
            return 
 
        if node.left and node.right:
            tmp, tmpParent = self._findBiggest(node.left)
            if tmpParent is not None:
                tmpParent.right = tmp.left
                tmp.left = node.left 
            tmp.right = node.right
        else:
            tmp = node.left or node.right
 
        if parent is None:
            self.root = tmp
        elif parent.left is node:
            parent.left = tmp
        else:
            parent.right = tmp


class HashTable:
    def __init__(self, table_capacity=163, hash_base=31415):
        self.table_capacity = table_capacity
        self.hash_base = hash_base
        self.count = 0
        self.table = [None] * table_capacity
  
    def __getitem__(self, key):
        hash = self.hash(key)
        if not self.table[hash]:
            raise KeyError
        else:
            res = self.table[hash].search()
            if res:
                return res.data
            else:
                raise KeyError

    def __setitem__(self, key, item):
        hash = self.hash(key)
        if self.table[hash]:
            self.table[hash].insert((key, item))
        else:
            t = BinarySearchTree()
            t.insert((key, item))
        self.count += 1

    def __contains__(self, key):
        hash = self.hash(key)
        if not self.table[hash]:
            return False
        else:
            res = self.table[hash].search()
            if res:
                return True
            else:
                raise False
    
    def hash(self, key):
        if not isinstance(key, str):
            raise TypeError
        value = 0
        for i in range(len(key)):
            value = (value*self.hash_base + ord(key[i])) % self.table_capacity
        return value

# import time

# def load_dictionary(hash_table, filename, time_limit=None):
#     start = time.time()
#     with open(filename, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             word = line.strip()
#             hash_table[word] = 1
#             if time_limit:
#                 duration = (time.time() - start)
#                 if duration >= time_limit:
#                     raise TimeoutError('Time out!')
#     return (time.time() - start)


# def load_dictionary_statistics(hash_base, table_size, filename, max_time):
#     hashtable = HashTable(table_capacity=table_size, hash_base=hash_base)
#     try:
#         duration = load_dictionary(hashtable, filename, max_time)
#         res = [hashtable.count, duration]
#         res.extend(hashtable.statistics())
#         return tuple(res)
#     except TimeoutError:
#         res = [hashtable.count, None]
#         res.extend(hashtable.statistics())
#         return tuple(res)

# def table_load_dictionary_statistics(max_time):
#     files = ('english_small.txt', 'english_large.txt', 'french.txt')
#     hash_bases = (1, 27183, 250726)
#     table_sizes = (250727, 402221, 1000081)
#     res = []
#     for file in files:
#         for hash_base in hash_bases:
#             for table_size in table_sizes:
#                 data = load_dictionary_statistics(hash_base, table_size, file, max_time)
#                 datas = [file, table_size, hash_base]
#                 datas.extend(data)
#                 datas = [str(d) for d in datas]
#                 res.append(datas)
#                 print(datas)
#     with open('output_task4.csv', 'w') as f:
#         for r in res:
#             line = ','.join(r)
#             f.write(line)
#             f.write('\n')

if __name__ == '__main__':
    # t = BinarySearchTree()
    # t.insert(('abc', 3))
    # t.insert(('ddu', 5))
    # t.insert(('kdiie', 7))
    # t.insert(('kdh83',1))
    # print(t.search(('kdiie', 7)).data)
    table_load_dictionary_statistics(120)
