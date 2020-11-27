import timeit
import task1

def load_dictionary(hash_table, filename, time_limit = 100):
    start = timeit.default_timer()
    file = open(filename, 'r')
    print("strings in the file: '")
    for line in file:
        val = line.strip('\n')
        print(len(val))
        hash_table[line.strip()] = 1
        time_taken = timeit.default_timer() - start
        if time_taken > time_limit:
            raise ValueError('too long bro.')
    file.close()
    print("'")
    return time_taken

def load_dictionary_time(hash_base, table_size, filename, max_time):
    pass
    #returns (words, time)
    #if time > max_time, then time is None
    table = task1.Hashtable(hash_base, table_size)

def table_load_dictionary_time(max_time):
    pass

h = task1.HashTable(7,3)
load_dictionary(h, 'words_empty.txt')
print(h.array)

