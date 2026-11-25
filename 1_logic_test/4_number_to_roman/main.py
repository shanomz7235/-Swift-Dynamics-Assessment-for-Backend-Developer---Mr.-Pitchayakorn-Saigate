"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_roman(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        if number == 0 or number > 3999:
            return "number must be between 1 and 3999"

        roman_map = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        result = ""
        for value, symbol in roman_map:
            print(f"Processing value: {value}, symbol: {symbol}, remaining number: {number}")  # Debugging line
            while number >= value:
                result += symbol
                number -= value

        return result


def main():
    solver = Solution()

    # Test Case
    test_cases = [101, -1, 0, 21, 258_987, 1_000_001, 10_000_000]
    print("--- Example Results ---")
    for num in test_cases:
        print(f"Input: {num}")
        print(f"Output: {solver.number_to_roman(num)}\n")

    # Input from user
    print("\n--- Please Input Number Between 0 and 10,000,000 ---")
    try:
        user_input = int(input("input: "))
        result = solver.number_to_roman(user_input)
        print(f"output: {result}")
    except ValueError:
        print("กรุณากรอกเป็นตัวเลขจำนวนเต็มเท่านั้น")


if __name__ == "__main__":
    main()
