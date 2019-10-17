import time
from task1 import HashTable

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
        return hashtable.count, None

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
    with open('output_task2.csv', 'w') as f:
        for r in res:
            line = ','.join(r)
            f.write(line)
            f.write('\n')

if __name__ == '__main__':
    table_load_dictionary_time(120)
    