# https://leetcode.com/problems/trapping-rain-water-ii/?envType=daily-question&envId=2025-01-19
class Solution:
    """
    Solution ot find trapped water
    """
    map: list[list[int]]

    def is_wall(self, x, y: int, bounder_x, bounder_y: int):
        """Check if the cell (x, y) is wall
        """
        if x == 0 or x == bounder_x - 1 or y == 0 or y == bounder_y - 1:
            return True
        return False
    
    def is_surrouned(self, x, y: int):
        t, r, b, l = self.map[]

    def trapRainWater(self, heightMap: list[list[int]]) -> int:
        """Find trapped water

        Args:
            heightMap (list[list[int]]): _description_

        Returns:
            int: _description_
        """
        if len(heightMap) < 3 or len(heightMap[0]) < 3:
            return 0

        self.map = heightMap
        
        bourder_y = len(heightMap)
        bounder_x = len(heightMap[0])
        for y, row in enumerate(heightMap):
            for x, cell in enumerate(row):
                print(f"{cell} ({x}-{y})", end=" ")
            print("\n")
                
                # print(x, y, self.is_wall(x, y, bounder_x, bourder_y))
        return 0


obj = Solution()
obj.trapRainWater([[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]])
