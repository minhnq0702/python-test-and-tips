# https://leetcode.com/problems/zigzag-conversion/description/
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [[] for _ in range(numRows)]
        current_row = 0
        direction = 1

        for char in s:
            rows[current_row].append(char)

            if current_row == 0:
                direction = 1
            elif current_row == numRows - 1:
                direction = -1

            current_row += direction

        return ''.join([''.join(row) for row in rows])


# Example usage:
solution = Solution()
print(solution.convert("PAYPALISHIRING", 3))  # Output: "PAHNAPLSIIGYIR"
print(solution.convert("PAYPALISHIRING", 4))  # Output: "PIN ALSIG YAHR PI"
print(solution.convert("A", 1))  # Output: "A"
