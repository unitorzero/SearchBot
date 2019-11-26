def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__, "%.3f" % (time.clock() - t), 'min')
        return res

    return wrapper
