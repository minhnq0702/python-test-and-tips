"""Hacker Earth Test"""
import time

from easy.equal_string import equal_strings
from easy.mex import find_mex
from easy.palindromic_string import palidromic_string

if __name__ == "__main__":
    start = time.time()
    palidromic_string()
    # find_mex()
    # equal_strings()
    print("===>", time.time() - start)
