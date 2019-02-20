import time

class Cache:
    def __init__(self):
        self.cache = {}
        self.lru = []

    def add_item(self, n, ret):
        if len(self.lru) > 50:
            del self.cache[self.lru[0]]
            self.cache[n] = ret
            self.lru = self.lru[1:].append(n)
        else:
            self.cache[n] = ret
            self.lru.append(n)

    def get_item(self, n):
        if n in self.lru:
            self.lru.remove(n)
            self.lru.append(n)
            return self.cache[n]
        else:
            return -1


def fib_recursion(n):
    if n in (0, 1):
        return 1
    else:
        return fib_recursion(n-1) + fib_recursion(n-2)


def fib_lru_cache(n, cache=None):
    if cache is None:
        cache = Cache()

    if n in (0, 1):
        return 1
    else:
        ret = cache.get_item(n)
        if ret == -1:
            ret = fib_lru_cache(n-1, cache) + fib_lru_cache(n-2, cache)
            cache.add_item(n, ret)

        return ret

def fib_cache(n, cache_all=None):
    if cache_all is None:
        cache_all = {}

    if n in (0, 1):
        return 1
    else:
        if n in cache_all:
            return cache_all[n]

        ret = fib_cache(n-1, cache_all) + fib_cache(n-2, cache_all)
        cache_all[n] = ret

        return ret

def fib_lst(n):
    cache = [1,1]
    if n in (0, 1):
        return 1
    for i in range(n-1):
        cache.append(cache[-1] + cache[-2])
    return cache[-1]

def fib_last(n):
    if n in (0, 1):
        return 1
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a+b
    return b

def timeit(fun, n, times):
    run_times = []
    for i in range(times):
        start = time.time()
        fun(n)
        run_times.append(time.time() - start)
    return sum(run_times) / times

def timethese(fun, n, times, total_times):
    rets = []
    for i in range(total_times):
        rets.append(timeit(fun, n, times))
    return rets


def main(n, filename='result.txt'):
    funs = [fib_recursion, fib_lru_cache, fib_cache, fib_lst, fib_last,]
    datas = []
    for fun in funs:
        data = timethese(fun, n, 50, 20)
        datas.append(data)

    with open(filename, 'w') as f:
        for data in datas:
            f.write('\t'.join([str(d) for d in data]))
            f.write('\n')
            f.write('\n')

if __name__ == '__main__':
    main(28)
