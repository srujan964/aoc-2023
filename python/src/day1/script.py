import re
import sys

if len(sys.argv) < 2:
    print("Usage: python script.pt input.txt")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, "r") as f:
    data = f.read().splitlines()

digits_spelled_out = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

digit_pattern = r"(\d|one|two|three|four|five|six|seven|eight|nine)"

conflicts = {
    "oneight": "one|eight",
    "twone": "two|one",
    "threeight": "three|eight",
    "fiveight": "five|eight",
    "sevenine": "seven|nine",
    "eightwo": "eight|two",
    "eighthree": "eight|three",
    "nineight": "nine|eight",
}


def part_one():
    calibration_vals = []
    for i in range(len(data)):
        digits = "".join(re.findall(r"\d+", data[i]))
        print(digits)
        if len(digits) == 1:
            val = int(digits[0]) * 11
            calibration_vals.append(val)
        else:
            val = int(f"{digits[0]}{digits[-1]}")
            calibration_vals.append(val)

    result = sum(calibration_vals)
    print(f"Result: {result}")


def parse_digit(value: str) -> int:
    if value in digits_spelled_out:
        return digits_spelled_out.index(value) + 1

    return int(value)


def part_two():
    calibration_vals = []
    for i in range(len(data)):
        text = data[i]
        for key in conflicts:
            if key in text:
                text = text.replace(key, conflicts[key])
        all_matches = re.findall(digit_pattern, text)
        val = (
            parse_digit(all_matches[0]) * 11
            if len(all_matches) == 1
            else (parse_digit(all_matches[0]) * 10) + parse_digit(all_matches[-1])
        )
        calibration_vals.append(val)

    result = sum(calibration_vals)
    print(f"Result: {result}")


part_two()
