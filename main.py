# encoding: utf-8
import functools
import random
import time


@functools.lru_cache(maxsize=2)
def test_func1(a: int, b: int) -> int:
    # res = int(random.random()) + a + b
    res = a + b
    print("def getting val==>", random.random(), res)
    return res

def is_palindrome(s: str) -> bool:
    return s == s[::-1]

def generate_palindromes(limit: int) -> list:
    palindromes = []
    for length in range(1, len(str(limit)) + 1):
        half_length = (length + 1) // 2
        for i in range(1, 10**half_length):
            half = str(i)
            if length % 2 == 0:
                palindrome = half + half[::-1]
            else:
                palindrome = half + half[-2::-1]
            
            palindrome_num = int(palindrome)
            if palindrome_num <= limit:
                palindromes.append(palindrome_num)
            else:
                break
    return palindromes

def count_superdrome(number) -> int:
    total = 0
    generated_pad = generate_palindromes(number)
    print('generated==>', generated_pad)

    for i in generated_pad:
        _str = str(i)
        bi_present = format(int(i), 'b')
        if is_palindrome(_str) and is_palindrome(bi_present):
            total += 1
    return total


def super_drome():
    number_of_query = input() # read number of queries
    input_queries = input() # read queries

    queries = input_queries.split(' ')
    res = []
    for idx in range(int(number_of_query)):
        superdromes = count_superdrome(int(queries[idx]))
        res.append(str(superdromes))

    print(' '.join(res))


import os
import typing
from threading import Thread, Timer


class Worker(object):
    __slot__ = "is_running",
    def __init__(self):
        self.is_running: bool = False

    def run(self, keep_track: dict):
        child_id = os.fork()
        if child_id:
            keep_track[child_id] = self
            return
        self.is_running = True
        while True:
            if not self.is_running:
                print("stopping....")
                time.sleep(1)
                break
            time.sleep(2)
            print(f"Hello world {os.getpid()}")

    def stop(self):
        self.is_running = False

def thread_timer_func(tracking):
    _worker = Worker()

    Timer(2, _worker.run, (tracking,)).start()


if __name__ == '__main__':
    # * super drome
    # super_drome()

    # * lru cache func
    # print(test_func1(1, 2))
    # print(test_func1(2, 3))
    # print(test_func1(1, 2))
    # print(test_func1(6, 7))
    # print(test_func1(1, 2))
    # print(test_func1(2, 3))

    workers: typing.Dict[int, Worker] = {}
    thread_timer_func(workers)
    print(f"Main process PID {os.getpid()}", workers)

    while 1:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for worker in workers.values():
                worker.stop()
            break
