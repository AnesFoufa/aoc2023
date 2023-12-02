#!/usr/bin/python3
from dataclasses import dataclass


@dataclass()
class Cubes:
    blue: int = 0
    red: int = 0
    green: int = 0

    def __le__(self, other: "Cubes"):
        return (
            self.blue <= other.blue
            and self.red <= other.red
            and self.green <= other.green
        )

    def power(self):
        return self.blue * self.red * self.green


def part_one(path):
    cubes_in_bag = Cubes(red=12, green=13, blue=14)
    res = 0
    with open(path, "r") as f:
        for line in f:
            game_str, cubes_strs = line.split(":")
            game_id = int(game_str.split()[1])
            if all(
                parse_cubes(cubes_str) <= cubes_in_bag
                for cubes_str in cubes_strs.split(";")
            ):
                res += game_id
    print(res)


def part_two(path):
    res = 0
    with open(path, "r") as f:
        for line in f:
            cubes_strs = line.split(":")[1].split(";")
            game = [parse_cubes(cubes_str) for cubes_str in cubes_strs]
            res += smallest_including_bag(game).power()
    print(res)


def parse_cubes(cubes_string: str) -> Cubes:
    res = Cubes()
    color_strings = cubes_string.split(",")
    for color_str in color_strings:
        nb, color = color_str.strip().split()
        if color == "blue":
            res.blue += int(nb)
        elif color == "green":
            res.green += int(nb)
        elif color == "red":
            res.red += int(nb)
        else:
            raise ValueError((cubes_string, color))
    return res


def smallest_including_bag(game: list[Cubes]):
    res = Cubes()
    for cubes in game:
        if res.red < cubes.red:
            res.red = cubes.red
        if res.blue < cubes.blue:
            res.blue = cubes.blue
        if res.green < cubes.green:
            res.green = cubes.green
    return res


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
