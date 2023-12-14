from itertools import chain

def part_one(path):
    with open(path, "r") as f:
        sum_nb_arrangements = 0
        for line in f:
            record, groups_str = line.strip().split()
            groups = [int(group_str) for group_str in groups_str.split(",")]
            nb_arrangements = compute_arrangements(record=record, groups=groups)
            sum_nb_arrangements += nb_arrangements
        print(sum_nb_arrangements)


def part_two(path):
    with open(path, "r") as f:
        sum_nb_arrangements = 0
        for line in f:
            record, groups_str = line.strip().split()
            groups = [int(group_str) for group_str in groups_str.split(",")]
            groups = groups * 5
            record = "?".join([record] * 5)
            nb_arrangements = compute_arrangements(record=record, groups=groups)
            sum_nb_arrangements += nb_arrangements
        print(sum_nb_arrangements)


def compute_arrangements(record: str, groups: list[int]) -> int:
    len_record = len(record)
    nb_groups = len(groups)

    dyn_matrix = [[0 for _ in range(len_record + 1)] for _ in range(nb_groups + 1)]
    dyn_matrix[0][-1] = 1
    reverse_groups_gen = chain([0], reversed(groups))

    for (i, group) in zip(range(nb_groups + 1), reverse_groups_gen):
        for j in reversed(range(len_record)):
            char = record[j]
            group_matches_record = i > 0 and matches(group, record[j:])
            j_prev = min([len_record, j + group + 1])
            match char:
                case ".":
                    dyn_matrix[i][j] = dyn_matrix[i][j + 1]
                case "#" if group_matches_record:
                    dyn_matrix[i][j] = dyn_matrix[i - 1][j_prev]
                case "?" if group_matches_record:
                    dyn_matrix[i][j] = dyn_matrix[i - 1][j_prev] + dyn_matrix[i][j + 1]
                case "?":
                    dyn_matrix[i][j] = dyn_matrix[i][j + 1]
    print(dyn_matrix)
    return dyn_matrix[-1][0]


def matches(group: int, record: str):
    len_record = len(record)
    return (
        len_record >= group
        and (len_record == group or record[group] in ".?")
        and all(char in "#?" for char in record[:group])
    )


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
