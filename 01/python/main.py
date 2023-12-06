#!/usr/bin/python3
import re


def part1():
    sum_calibration_values = 0
    with open("../input.txt", "r") as f:
        for line in f:
            digits = [char for char in line if str.isdigit(char)]
            calibration_value = int(digits[0] + digits[-1])
            sum_calibration_values += calibration_value
    print(sum_calibration_values)


digits_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part2():
    digits_pattern = re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|[1-9]))")
    sum_calibration_values = 0
    with open("../input.txt", "r") as f:
        for line in f:
            spelled_digits = digits_pattern.findall(line)
            first_spelled_digit, last_spelled_digit = (
                spelled_digits[0],
                spelled_digits[-1],
            )
            first_digit = digits_map.get(first_spelled_digit, first_spelled_digit)
            last_digit = digits_map.get(last_spelled_digit, last_spelled_digit)
            calibration_value = int(first_digit + last_digit)
            sum_calibration_values += calibration_value
    print(sum_calibration_values)


if __name__ == "__main__":
    part1()
    part2()
