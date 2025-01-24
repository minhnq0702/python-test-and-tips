# https://leetcode.com/problems/roman-to-integer/
ROMAIN_TO_INT = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

class Solution:
    # def romanToInt(self, s: str) -> int:
    #     for i in range(len(s)):
    #         if i == 0:
    #             continue
    #         if ROMAIN_TO_INT[s[i]] > ROMAIN_TO_INT[s[i-1]]:
    #             ROMAIN_TO_INT[s[i-1]] *= -1

    #     return sum(ROMAIN_TO_INT[c] for c in s)

    def romanToInt(self, s: str) -> int:
        vals = []
        for c in s:
            _val = ROMAIN_TO_INT[c]
            if vals and vals[-1] < _val:
                vals[-1] *= -1
            vals.append(_val)
        return sum(vals)
    
obj = Solution()
print(obj.romanToInt("MCMXCIV"))