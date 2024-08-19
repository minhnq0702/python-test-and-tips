"""Hacker Earth Test"""
import time

# pylint: disable=E0401,W0611
from level_easy.mex import find_mex
from level_easy.palindromic_string import palidromic_string
from level_medium.equal_string import equal_strings

# pylint: disable=W0611

if __name__ == "__main__":
    start = time.time()

    # palidromic_string()
    # find_mex()
    equal_strings()

    print("===>", time.time() - start)
