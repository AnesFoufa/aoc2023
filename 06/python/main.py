from math import sqrt, ceil, floor, prod


def part_one(path):
    with open(path, "r") as f:
        file_lines = f.readlines()

    durations = [
        int(duration_str) for duration_str in file_lines[0].split(":")[1].split()
    ]
    records = [int(record_str) for record_str in file_lines[1].split(":")[1].split()]

    prod_solutions = prod(
        compute_nb_solutions(duration=duration, record=record)
        for (duration, record) in zip(durations, records)
    )
    print(prod_solutions)


def part_two(path):
    with open(path, "r") as f:
        file_lines = f.readlines()

    duration = int(file_lines[0].split(":")[1].replace(" ", ""))
    record = int(file_lines[1].split(":")[1].replace(" ", ""))

    print(compute_nb_solutions(duration=duration, record=record))


def compute_nb_solutions(duration: int, record: int):
    delta = duration**2 - 4 * record
    if delta < 0:
        nb_solutions = 0
    else:
        sqrt_delta = sqrt(delta)

        duration_min = (duration - sqrt_delta) / 2
        bound1 = floor(duration_min + 1)

        duration_max = (duration + sqrt_delta) / 2
        bound2 = ceil(duration_max - 1)

        nb_solutions = bound2 - bound1 + 1
    return nb_solutions


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
