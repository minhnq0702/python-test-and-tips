# encoding: utf-8
import random
import functools


@functools.lru_cache(maxsize=2)
def test_func1(a: int, b: int) -> int:
    # res = int(random.random()) + a + b
    res = a + b
    print("def getting val==>", random.random(), res)
    return res

if __name__ == '__main__':
    print('Hello, World!')
    print(test_func1(1, 2))
    print(test_func1(2, 3))
    print(test_func1(1, 2))
    print(test_func1(6, 7))
    print(test_func1(1, 2))
    print(test_func1(2, 3))
    print(test_func1.cache_info())
