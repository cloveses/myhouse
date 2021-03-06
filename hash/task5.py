#!/usr/bin/python3

class BinaryTreeNode:

    def __init__(self, key=None, value=None, left=None, right=None):
        self.key = key
        self.item = value
        self.left = left
        self.right = right

    def __str__(self):
        return " (" + str(self.key) +  ", " + str(self.item) + " ) "


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def __len__(self):
        return self._len_aux(self.root)

    def _len_aux(self,current):
        if current is None:
            return 0
        else:
            return 1+self._len_aux(current.left)+self._len_aux(current.right)

    def inorder(self,f):
        return self._inorder_aux(self.root,f)

    def _inorder_aux(self,current,f):
        if current is not None:
            self._inorder_aux(current.left, f)
            f(current)
            self._inorder_aux(current.right, f)

    def __contains__(self, key):
        #return self._contains_aux(key, self.root)
        return self._contains_iter(key)

    def _contains_aux(self, key, current_node):
        if current_node is None:  # base case
            return False
        elif key == current_node.key:
                return True
        elif key < current_node.key:
            return self._contains_aux(key, current_node.left)
        elif key > current_node.key:
            return self._contains_aux(key, current_node.right)

    def _contains_iter(self, key):
        current_node = self.root
        while current_node is not None:
            if key < current_node.key:
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
            else:
                return True
        return False

    def __getitem__(self, key):
        return self._get_item_iter(key, self.root)

    def _get_item_aux(self, key, current_node):
        if current_node is None:  # base case
            raise KeyError("Key not found")
        elif key == current_node.key:
                return current_node.item
        elif key < current_node.key:
            return self._get_item_aux(key, current_node.left)
        elif key > current_node.key:
            return self._get_item_aux(key, current_node.right)

    def _get_item_iter(self, key, current_node):
        while current_node is not None:
          if key < current_node.key:
            current_node = current_node.left
          elif key > current_node.key:
            current_node = current_node.right
          else:
            assert current_node.key == key
            return current_node.item
        raise KeyError("Key not found")

    def __setitem__(self, key, value):
        self._insert_iter(key, value)

    def _insert_aux(self, key, value, current_node):
        if current_node is None:
            current_node = BinaryTreeNode(key, value)
        elif key < current_node.key:
            current_node.left =  self._insert_aux(key, value, current_node.left)
        elif key > current_node.key:
            current_node.right = self._insert_aux(key, value, current_node.right)
        elif key == current_node.key:
            current_node.item = value
        return current_node

    def _insert_iter(self, key, value):
        if self.root is None:
            self.root = BinaryTreeNode(key, value)
            return

        current_node = self.root
        while True:
          if key < current_node.key:
            if current_node.left is None:
              current_node.left = BinaryTreeNode(key, value)
              break
            else:
              current_node = current_node.left
          elif key > current_node.key:
            if current_node.right is None:
              current_node.right = BinaryTreeNode(key, value)
              break
            else:
              current_node = current_node.right
          else:
            assert current_node.key == key
            current_node.item = item
            break


class HashTable:
    def __init__(self, table_capacity=31163, hash_base=31415):
        self.table_capacity = table_capacity
        self.hash_base = hash_base
        self.count = 0
        self.table = [None] * table_capacity
  
    def __getitem__(self, key):
        hash = self.hash(key)
        # hash位置为None，则直接报错
        if not self.table[hash]:
            raise KeyError
        else:
            # hash位置不为None，到bst中查找对应key
            bst = self.table[hash]
            if key in bst:
                return bst[key]
            else:
                raise KeyError

    def __setitem__(self, key, item):
        hash = self.hash(key)
        # hash位置不为None，则直接插入该位置的bst
        if self.table[hash]:
            self.table[hash][key] = item
        else:
            # hash位置为None，则先创建bst并插入数据后保存至hash位置
            t = BinarySearchTree()
            t[key] = item
            self.table[hash] = t
        self.count += 1

    def __contains__(self, key):
        hash = self.hash(key)
        # hash位置为None，则说明不存在
        if not self.table[hash]:
            return False
        else:
            # hash位置不为None，则判断是否在对应位置的bst中
            if key in self.table[hash]:
                return True
            else:
                return False
    
    def hash(self, key):
        if not isinstance(key, str):
            raise TypeError
        value = 0
        for i in range(len(key)):
            value = (value*self.hash_base + ord(key[i])) % self.table_capacity
        return value

import time

def load_dictionary(hash_table, filename, time_limit=None):
    # 开始计时
    start = time.time()
    # 打开文件并逐行添加到hash表
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip()
            hash_table[word] = 1
            # 如果有时间限制则检查是否超时，超时则发生错误
            if time_limit:
                duration = (time.time() - start)
                if duration >= time_limit:
                    raise TimeoutError('Time out!')
    return (time.time() - start)

def load_dictionary_time(hash_base, table_size, filename, max_time):
    # 创建hash表
    hashtable = HashTable(table_capacity=table_size, hash_base=hash_base)
    # 处理异常
    try:
        duration = load_dictionary(hashtable, filename, max_time)
        return hashtable.count, duration
    except TimeoutError:
        return hashtable.count, 'timeout'

def table_load_dictionary_time(max_time):
    files = ('english_small.txt', 'english_large.txt', 'french.txt')
    hash_bases = (1, 27183, 250726)
    table_sizes = (250727, 402221, 1000081)
    res = []
    # 循环应用数据处理
    for file in files:
        for hash_base in hash_bases:
            for table_size in table_sizes:
                words, duration = load_dictionary_time(hash_base, table_size, file, max_time)
                res.append((file, str(table_size), str(hash_base), str(words), str(duration)))
                print((file, str(table_size), str(hash_base), str(words), str(duration)))
    # 写入数据文件
    with open('output_task5.csv', 'w') as f:
        for r in res:
            line = ','.join(r)
            f.write(line)
            f.write('\n')

if __name__ == '__main__':
    table_load_dictionary_time(60)