# https://leetcode.com/problems/reverse-integer/
class Solution:
    def reverse(self, x: int) -> int:
        if x == 0:
            return 0

        sign = 1
        if x < 0:
            sign = -1
        
        x = abs(x)
        res = 0
        while x:
            i = x % 10
            res = res * 10 + i
            x //= 10

        res *= sign
        if pow(-2, 31) > res or res >= pow(2, 31):
            return 0

        return res