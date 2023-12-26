from sys import argv
from itertools import pairwise
from typing import Callable


Point = tuple[int, int]


def part_one(path):
    solve(path=path, parse_line=parse_direction_length_part1)


def part_two(path):
    solve(path=path, parse_line=parse_direction_length_part2)


def solve(path, parse_line):
    points, length = read_outline_length(path, parse_line)
    area = shoelace(points)
    print(int(area - 0.5 * length + 1) + length)


def read_outline_length(path, parse_direction_length: Callable[[str], tuple[str, int]]):
    with open(path, "r") as f:
        x, y = 0, 0
        length = 0
        outline: list[Point] = [(x, y)]
        for line in f:
            direction, nb = parse_direction_length(line)
            length += nb
            match direction:
                case "R":
                    x += nb
                case "L":
                    x -= nb
                case "D":
                    y += nb
                case "U":
                    y -= nb

                case _:
                    raise ValueError()
            outline.append((x, y))
        return outline, length


def shoelace(x_y):
    area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in pairwise(x_y)) / 2
    return area


def parse_direction_length_part1(line: str):
    direction, length_str, _ = line.split()
    length = int(length_str)
    return direction, length


def parse_direction_length_part2(line: str):
    hex_str = line.strip().split()[-1].strip("()#")
    match int(hex_str[-1]):
        case 0:
            direction = "R"
        case 1:
            direction = "D"
        case 2:
            direction = "L"
        case 3:
            direction = "U"
        case _:
            raise ValueError(hex_str)
    length = int(hex_str[:-1], 16)
    return direction, length


if __name__ == "__main__":
    path = argv[1]
    part_one(path=path)
    part_two(path=path)
