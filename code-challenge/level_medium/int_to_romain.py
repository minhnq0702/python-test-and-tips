# https://leetcode.com/problems/integer-to-roman/description/
INT_TO_ROMAIN = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    90: "XC",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I",
}


class Solution:
    def intToRoman(self, num: int) -> str:
        romains = ""
        for int_key, val in INT_TO_ROMAIN.items():
            print("[minhne]", f"{int_key}")
            while num >= int_key:
                romains += val
                num -= int_key
        return romains


res = Solution().intToRoman(3749)
print("[minhne]", f"{res}")
