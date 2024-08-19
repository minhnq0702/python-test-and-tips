"""
https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/find-mex-62916c25/
Find minimal excluded
"""
def find_mex():
    """
    Input and find Mex
    """
    # n = int(input())
    # lst_str = input()
    with open("./easy/mex.txt", "r", encoding="utf-8") as f:
        arr = f.readlines()
    n = arr[0]
    lst_str = arr[1]

    lst = map(int, lst_str.strip().split(" "))
    mex = 0
    res = []
    passed = set()
    for i in lst:
        if i in passed:
            res.append(str(mex))
            continue
        passed.add(i)
        while mex == i or mex in passed:
            mex += 1
        res.append(str(mex))

    print(" ".join(res))
