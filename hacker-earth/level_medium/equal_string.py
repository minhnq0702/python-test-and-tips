"""
https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/equal-strings-79789662-4dbd707c/
Equalize 2 binary string by flip element
"""

# TODO: need to refactor. it does running incorect for some testcase

def get_min_diff(diff: list[int], cost):
    """Get min diff

    Args:
        diff (list[int]): array of diff postion

    Returns:
        typle[int, int, int]: diff value, diff pos 1, diff pos 2
    """
    min_diff = -1
    low_idx = -1
    high_idx = -1
    for i in range(len(diff) - 1):
        diff_val = diff[i+1] - diff[i]
        if min_diff == -1 or diff_val < min_diff:
            min_diff = diff_val
            low_idx = i
            high_idx = i+1

    return expand_bounder(diff, low_idx, high_idx, min_diff, cost)


def expand_bounder(diff, low, high, total_cost, cost):
    """
    Eg:  65, 70, 72, 74 / cost = 6
    low = 70
    high = 72
    total_cost = 2
    lower_cost = (70 - 65) = 5
    higher_cost = (74 - 72) = 2
    1/ cost to remove low - high => remove lower - higher = total_cost + min(higher - lower, cost) = 2 + min(74 - 65, 6) = 8
    2/ cost to remove lower - low / high - higer = min(low - lower, 6) + min(higher - high, 6) = min(70 - 65) + min(74 - 72) = 7
    So, get select 2 and return
    """
    if low == 0 or high == len(diff) - 1 or (high - low) > cost:
        return [(diff[low], diff[high])]
    lower = low - 1
    higher = high + 1
    lower_cost = min(abs(diff[low] - diff[lower]), cost)
    higher_cost = min(abs(diff[higher] - diff[high]), cost)
    total_cost += min(diff[higher] - diff[lower], cost)

    if (lower_cost + higher_cost) < total_cost:
        return [(diff[lower], diff[low]), (diff[high], diff[higher])]
    return [(diff[low], diff[high])]


def equal_strings():
    # cost = int(input().strip())
    # s1 = input()
    # s2 = input()
    cost = 6
    s1 = "10010 00000  1 10001 1100 0000110  0100010101000011001111010001111101101010100001110010"  # 1 + 3 + 3
    s2 = "10001 10001  1 00000 1100 1000111  0100011101100010001011011011111001101000101001110110"

    cost = 7
    s1 = "01101100000100011000010011011100100000110101110100001111101100010100001110110111100100111100011001"  # ==> 30
    s2 = "11101110101100010000010001011101101000110111110100101101001100011100100111111111100110111110011011"

    if s1 == s2:
        print(0)
        return

    total_cost = 0
    diff = set()
    for i, c in enumerate(s1):
        if c != s2[i]:
            diff.add(i)

    diff = sorted(list(diff))
    if len(diff) % 2 == 1:
        print(-1)
        return

    while diff:
        for low, high in get_min_diff(diff, cost):
            total_cost += min(high - low, cost)
            diff.remove(low)
            diff.remove(high)
        if not diff:
            break

    print(total_cost)

