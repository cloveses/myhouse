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

