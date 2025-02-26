# https://leetcode.com/problems/container-with-most-water/
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        if len(height) < 2:
            return 0

        if len(height) == 2:
            return min(height)

        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            max_area = max(max_area, min(
                height[left], height[right]) * (right - left))

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area


res = Solution().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7])
print("[minhne]", f"{res}")
