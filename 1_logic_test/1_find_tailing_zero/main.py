"""
เขียบนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""


class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        if number < 0:
            return "number can not be negative"

        count = 0
        while number >= 5:
            number //= 5
            count += number

        return count


if __name__ == "__main__":
    sol = Solution()

    number = int(input("input : "))
    print(f"output : {sol.find_tailing_zeroes(number)}")

    ## !----- Test cases ------
    # print("----------Test cases----------")
    # print(f"Input : 7\nOutput: {sol.find_tailing_zeroes(7)}\n")
    # print(f"Input : 10\nOutput: {sol.find_tailing_zeroes(10)}\n")
    # print(f"Input : 25\nOutput: {sol.find_tailing_zeroes(25)}\n")
    # print(f"Input : 0\nOutput: {sol.find_tailing_zeroes(0)}\n")
    # print(f"Input : -5\nOutput: {sol.find_tailing_zeroes(-5)}\n")