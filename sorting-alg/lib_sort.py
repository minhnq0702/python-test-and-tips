# -*- encoding: utf-8 -*-
"""Lib sort"""
from time import time

from numpy import random


def library_sort(n: int):
    """Sort by python-library

    Args:
        n (int): size of testcase
    """
    testcase = random.randint(1000, size=n)
    start = time()
    testcase.sort()
    print(f"Time of sorting with numpy: {time() - start}")
