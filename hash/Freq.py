#!/usr/bin/env python3
"""
:author: Graeme Gange
"""
from task1 import HashTable
class Freq:
    def __init__(self):
        self.word_frequency = HashTable()
  
    def add_file(self, filename):
        raise NotImplementedError

    def rarity(self, word):
        raise NotImplementedError

    def compare(self, other_filename):
        raise NotImplementedError
