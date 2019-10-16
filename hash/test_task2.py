from task1 import HashTable
from task2 import load_dictionary

for file in ('words.txt', 'wordsb.txt', 'wordsc.txt'):
    hashtable = HashTable()
    print(load_dictionary(hashtable, file,  time_limit=30))