# https://leetcode.com/problems/water-and-jug-problem/description/
# pylint: skip-file
from math import gcd


class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        if x + y < target:
            return False
        
        if x == target or y == target or x + y == target:
            return True
        
        return target % gcd(x, y) == 0

    def canMeasureWareDFS(self, x: int, y: int, target: int) -> bool:
        if x + y < target:
            return False
        
        if x == target or y == target or x + y == target:
            return True
        
        visited = set()
        
        def dfs(a, b: int) -> bool:
            if a > x:
                a = x
            if b > y:
                b = y

            if (a, b) in visited:
                return False
            
            if a + b == target:
                return True

            visited.add((a, b))
            
            return (
                dfs(x, b) or 
                dfs(a, y) or 
                dfs(0, b) or 
                dfs(a, 0) or 
                dfs(min(x, a + b), b - min(x, a + b)) or # đổ nước từ bình 2 sang bình 1
                dfs(a - min(y, a + b), min(y, a + b)))
        
        return dfs(0, 0)
    
res = Solution().canMeasureWareDFS(3, 5, 4) # True
print(res)
