# encoding: utf-8
import functools
import random


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


if __name__ == '__main__':
    super_drome()
    print(test_func1(1, 2))
    print(test_func1(2, 3))
    print(test_func1(1, 2))
    print(test_func1(6, 7))
    print(test_func1(1, 2))
    print(test_func1(2, 3))
