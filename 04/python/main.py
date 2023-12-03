from collections import deque


def part_one(path):
    total_points = 0

    with open(path, "r") as f:
        for line in f:
            nb_winning_numbers = nb_winning(line)
            if nb_winning_numbers:
                total_points += 2 ** (nb_winning_numbers - 1)

    print(total_points)


def part_two(path):
    nb_cards = 0

    copies = deque()
    with open(path, "r") as f:
        for line in f:
            nb_copies = 1
            try:
                nb_copies += copies.popleft()
            except IndexError:
                pass
            nb_cards += nb_copies

            nb_winning_numbers = nb_winning(line)

            for i in range(nb_winning_numbers):
                try:
                    copies[i] += nb_copies
                except IndexError:
                    copies.append(nb_copies)

    print(nb_cards)


def nb_winning(line):
    res = 0
    cards_str = line.split(":")[1]
    winning_numbers_str, my_numbers_str = cards_str.strip().split("|")
    winning_numbers = {int(number_str) for number_str in winning_numbers_str.split()}
    for number_str in my_numbers_str.split():
        if int(number_str) in winning_numbers:
            res += 1
    return res


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
