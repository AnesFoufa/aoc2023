#!/usr/bin/python3
from dataclasses import dataclass
from typing import Tuple
import re


@dataclass()
class Number:
    val: int
    row: int
    col: int
    width: int

    def is_adjacent(self, row: int, col: int):
        return -1 <= row - self.row <= 1 and -1 <= col - self.col <= self.width


def part_one(path):
    sum_part_numbers = 0

    numbers: list[Number] = []
    symbols: list[Tuple[int, int]] = []
    pattern = re.compile(r"(\d+|[^.])")
    with open(path, "r") as f:
        for (row, line) in enumerate(f):
            parse_numbers_and_symbols(row, line, pattern, numbers, symbols)

    for number in numbers:
        if is_part(number, symbols):
            sum_part_numbers += number.val

    print(sum_part_numbers)


def part_two(path):
    sum_gear_ratios = 0

    numbers: list[Number] = []
    gears: list[Tuple[int, int]] = []
    pattern = re.compile(r"(\d+|\*)")
    with open(path, "r") as f:
        for (row, line) in enumerate(f):
            parse_numbers_and_symbols(row, line, pattern, numbers, gears)

    for (row, col) in gears:
        adjacent_to_current_gear: list[Number] = []
        for number in numbers:
            if number.is_adjacent(row, col):
                adjacent_to_current_gear.append(number)
                if len(adjacent_to_current_gear) > 2:
                    break
        if len(adjacent_to_current_gear) == 2:
            sum_gear_ratios += (
                adjacent_to_current_gear[0].val * adjacent_to_current_gear[1].val
            )

    print(sum_gear_ratios)


def parse_numbers_and_symbols(row, line, pattern, numbers, symbols):
    for match_o in pattern.finditer(line.strip()):
        string = match_o.group()
        col_start, col_end = match_o.span()
        if string[0].isdigit():
            width = col_end - col_start
            numbers.append(Number(val=int(string), row=row, col=col_start, width=width))
        else:
            symbols.append((row, col_start))


def is_part(number: Number, symbols):
    return any(number.is_adjacent(row, col) for (row, col) in symbols)


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
