#!/usr/bin/python3
from dataclasses import dataclass
from typing import Tuple, Callable


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
    with open(path, "r") as f:
        for (row, line) in enumerate(f):
            parse_numbers_and_symbols(row, line, is_symbol, numbers, symbols)

    for number in numbers:
        if is_part(number, symbols):
            sum_part_numbers += number.val

    print(sum_part_numbers)


def part_two(path):
    sum_gear_ratios = 0

    numbers: list[Number] = []
    gears: list[Tuple[int, int]] = []
    with open(path, "r") as f:
        for (row, line) in enumerate(f):
            parse_numbers_and_symbols(row, line, is_gear, numbers, gears)

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


def parse_numbers_and_symbols(
    row: int,
    line: str,
    is_symbol: Callable[[str], bool],
    numbers: list[Number],
    symbols: list[Tuple[int, int]],
):
    parsing_number = False
    val = 0
    start_col = 0

    for (col, char) in enumerate(line.strip()):
        if char.isdigit():
            if not parsing_number:
                start_col = col
            parsing_number = True
            val = val * 10 + int(char)
        else:
            if parsing_number:
                numbers.append(
                    Number(val=val, row=row, col=start_col, width=col - start_col)
                )
            if is_symbol(char):
                symbols.append((row, col))
            parsing_number = False
            val = 0
    if parsing_number:
        numbers.append(Number(val=val, row=row, col=start_col, width=col - start_col))


def is_part(number: Number, symbols):
    return any(number.is_adjacent(row, col) for (row, col) in symbols)


def is_symbol(char: str):
    return char != "."


def is_gear(char: str):
    return char == "*"


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
