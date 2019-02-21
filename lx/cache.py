def add_cache(fun):
    cache = {}
    def wrapper(n):
        print(cache)
        if n in cache:
            return cache[n]
        else:
            cache[n] = fun(n)
            return cache[n]
    return wrapper

@add_cache
def fib_cache(n):
    if n in (0, 1):
        return 1
    else:
        return fib_cache(n-1) + fib_cache(n-2)

if __name__ == '__main__':
    print(fib_cache(10))