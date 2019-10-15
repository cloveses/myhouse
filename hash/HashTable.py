#!/usr/bin/env python3
"""
:author: Graeme Gange
"""

class HashTable:
    def __init__(self, table_capacity, hash_base): 
        self.table = [None] * table_capacity
        self.base = hash_base
        self.count = 0
  
    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, item):
        raise NotImplementedError

    def __contains__(self, key):
        raise NotImplementedError

    def hash(self, key):
        raise NotImplementedError

    def rehash(self):
        raise NotImplementedError
