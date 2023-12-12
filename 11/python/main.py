def part_one(path):
    solve(path=path, expansion_factor=2)


def part_two(path):
    solve(path=path, expansion_factor=1_000_000)


def solve(path, expansion_factor):
    mult_factor = expansion_factor - 1
    with open(path, "r") as f:
        lines = [line.strip() for line in f]
    nb_rows = len(lines)
    nb_cols = len(lines[0])
    empty_cols = set(range(nb_cols))
    empty_rows = set(range(nb_rows))
    galaxies = set()

    for (i, line) in enumerate(lines):
        for (j, char) in enumerate(line):
            if char == "#":
                galaxies.add((i, j))
                if i in empty_rows:
                    empty_rows.remove(i)
                if j in empty_cols:
                    empty_cols.remove(j)

    distances = {}
    for (i1, j1) in galaxies:
        for (i2, j2) in galaxies:
            pair = frozenset({(i1, j1), (i2, j2)})
            if (i1, j1) != (i2, j2) and pair not in distances:
                raw_distance = abs(i2 - i1) + abs(j2 - j1)
                empty_rows_between = [
                    i for i in range(*sorted([i1, i2])) if i in empty_rows
                ]
                empty_cols_between = [
                    i for i in range(*sorted([j1, j2])) if i in empty_cols
                ]
                adjusted_distance = raw_distance + mult_factor * (
                    len(empty_rows_between) + len(empty_cols_between)
                )
                distances[pair] = adjusted_distance
    print(sum(distances.values()))


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
