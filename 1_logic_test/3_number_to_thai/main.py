"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:
    def number_to_thai(self, number: int) -> str:
        # ตรวจสอบเงื่อนไขขอบเขตตัวเลข
        if number < 0:
            return "number can not less than 0"
        if number > 10_000_000:
            return "number can not more than 10,000,000"
        if number == 0:
            return "ศูนย์"

        thai_digits = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        thai_units = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

        def convert_under_million(num: int) -> str:
            text = ""
            num_str = str(num)
            length = len(num_str)

            for i, char in enumerate(num_str):
                digit = int(char)
                # ย้อนหลังจากซ้ายไปขวา เป็นจากขวามาซ้าย
                unit_pos = length - i - 1

                if digit == 0:
                    continue

                if unit_pos == 1:
                    if digit == 1:
                        text += "สิบ"
                    elif digit == 2:
                        text += "ยี่สิบ"
                    else:
                        text += thai_digits[digit] + "สิบ"
                elif unit_pos == 0:
                    if digit == 1 and length > 1:
                        tens = (num // 10) % 10
                        if tens != 0:
                            text += "เอ็ด"
                        else:
                            text += thai_digits[digit]
                    else:
                        text += thai_digits[digit]
                else:
                    text += thai_digits[digit] + thai_units[unit_pos]

            return text

        if number >= 1_000_000:
            millions = number // 1_000_000
            remainder = number % 1_000_000
            result = convert_under_million(millions) + "ล้าน"
            if remainder > 0:
                result += convert_under_million(remainder)
            return result

        return convert_under_million(number)


def main():
    solver = Solution()

    # Test Case
    test_cases = [101, -1, 0, 21, 258_987, 1_000_001, 10_000_000]
    print("--- Example Results ---")
    for num in test_cases:
        print(f"Input: {num}")
        print(f"Output: {solver.number_to_thai(num)}\n")

    # Input from user
    print("\n--- Please Input Number Between 0 and 10,000,000 ---")
    try:
        user_input = int(input("input: "))
        result = solver.number_to_thai(user_input)
        print(f"output: {result}")
    except ValueError:
        print("กรุณากรอกเป็นตัวเลขจำนวนเต็มเท่านั้น")


if __name__ == "__main__":
    main()

