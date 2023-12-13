def part_one(path):
    solve(path, smudge=False)


def part_two(path):
    solve(path, smudge=True)


def solve(path, smudge):
    summary = 0
    with open(path, "r") as f:
        file_content = f.read().strip()

    for pattern_str in file_content.split("\n\n"):
        pattern_lines = pattern_str.split("\n")
        column = (
            reflection_column_smudge(pattern_lines=pattern_lines)
            if smudge
            else reflection_column(pattern_lines=pattern_lines)
        )
        if not column:
            pattern_cols = transpose(pattern_lines)
            row = (
                reflection_column_smudge(pattern_lines=pattern_cols)
                if smudge
                else reflection_column(pattern_lines=pattern_cols)
            )

        else:
            row = 0
        summary += column + 100 * row
    print(summary)


def reflection_column(pattern_lines: list[str]) -> int:
    nb_cols = len(pattern_lines[0])
    for j in range(1, nb_cols):
        for line in pattern_lines:
            length = min([j, nb_cols - j])
            line1 = line[j - length : j]
            line2 = line[j + length - 1 : j - 1 : -1]
            if line1 != line2:
                break
        else:
            return j
    return 0


def reflection_column_smudge(pattern_lines: list[str]) -> int:
    nb_cols = len(pattern_lines[0])
    for j in range(1, nb_cols):
        nb_smudges = 0
        for line in pattern_lines:
            length = min([j, nb_cols - j])
            line1 = line[j - length : j]
            line2 = line[j + length - 1 : j - 1 : -1]
            for (ch1, ch2) in zip(line1, line2):
                if ch1 != ch2:
                    nb_smudges += 1
                    if nb_smudges > 1:
                        break
            else:
                continue
            break
        else:
            if nb_smudges == 1:
                return j
    return 0


def transpose(pattern_lines: list[str]) -> list[str]:
    nb_cols = len(pattern_lines[0])
    transposed_lines = [[] for _ in range(nb_cols)]
    for line in pattern_lines:
        for (j, char) in enumerate(line):
            transposed_lines[j].append(char)
    return ["".join(line) for line in transposed_lines]


if __name__ == "__main__":
    part_two("../input.txt")
