"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        if len(numbers) == 0:
            return "list can not blank"
        max_value = max(numbers)
        return numbers.index(max_value)

def main():
    sol = Solution()

    # # !----- Test cases ------
    # print("----------Test cases----------")
    # print(f"Input : [1,2,1,3,5,6,4]\nOutput: {sol.find_max_index([1,2,1,3,5,6,4])}\n")
    # print(f"Input : [10,20,30,40,50]\nOutput: {sol.find_max_index([10,20,30,40,50])}\n")
    # print(f"Input : []\nOutput: {sol.find_max_index([])}\n")

    numbers = list(map(int, input("numbers: ").split()))
    print(f"output : {sol.find_max_index(numbers)}")

    
if __name__ == "__main__":
    main()
    
    
    

   