# https://leetcode.com/problems/find-pivot-index/
class Solution:
    def pivotIndex(self, nums: list[int]) -> int:
        sum_l = 0
        sum_r = sum(nums[1:])
        if sum_l == sum_r:
            return 0

        for i in range(len(nums)):
            if i == 0:
                continue
            sum_l += nums[i-1]
            sum_r -= nums[i]
            if sum_l == sum_r:
                return i

        return -1


obj = Solution()
print(obj.pivotIndex([-1, -1, -1, 1, 1, 1]))
