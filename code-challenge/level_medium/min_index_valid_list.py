from collections import Counter
from typing import List


def minimum_index(nums: List[int]) -> int:
    """
    Finds the minimum index such that the dominant element in the list is
    still dominant in both the left and right sublists.

    Args:
        nums (List[int]): _description_

    Returns:
        int: _description_
    """
    _counter: tuple = Counter(nums).most_common(1)[0]

    dom_freq = _counter[1]
    dom_el = _counter[0]
    dom_total = dom_freq * 2
    res = -1
    left_freq = 0
    for i, el in enumerate(nums):
        if i > len(nums) - 1:
            break
        if el != dom_el:
            continue

        left_freq += 1
        left_dom = left_freq * 2
        if (left_dom > i+1) and (dom_total - left_dom) > len(nums) - (i+1):
            res = i
            break
    return res

print(minimum_index([1,1,1]))
