from collections import defaultdict
from colorama import init


def part_one(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f]
    graph, start_pos, _, _ = read_graph(lines=lines)

    distances_from_start = {start_pos: 0}
    stack = [start_pos]
    while stack:
        pos = stack.pop()
        distance = distances_from_start[pos]
        for neighboring_pos in graph[pos]:
            if (neighboring_pos not in distances_from_start) or (
                distances_from_start[neighboring_pos] > distance + 1
            ):
                distances_from_start[neighboring_pos] = distance + 1
                stack.append(neighboring_pos)

    print(max(distances_from_start.values()))


def part_two(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f]
    graph, start_pos, nb_rows, nb_cols = read_graph(lines=lines)

    # Extract the pipe (cycle detection via DFS)
    pipe_set = {start_pos}
    stack = []
    prev_positions = {}
    for next_pos in graph[start_pos]:
        stack.append(next_pos)
        prev_positions[next_pos] = start_pos
    while stack:
        pos = stack.pop()
        prev_pos = prev_positions[pos]
        for next_pos in graph[pos]:
            if next_pos == prev_pos:
                continue
            if next_pos == start_pos:
                while pos != start_pos:
                    pipe_set.add(pos)
                    pos = prev_positions[pos]
                break
            prev_positions[next_pos] = pos
            stack.append(next_pos)
        else:
            continue
        break

    # Compute enclosed area, diagonal ray from each point, if crosses the the enclosure an odd number of times, it is outside
    enclosed_area = set()
    enclosed_count = 0
    for i, line in enumerate(lines):
        for j, _ in enumerate(line):
            if (i, j) in pipe_set:
                continue

            # The edges L and 7 are not crossed by the ray
            diagonal_ray = [
                lines[i2][j2]
                for (i2, j2) in zip(range(i, nb_rows), range(j, nb_cols))
                if (i2, j2) in pipe_set and lines[i2][j2] not in "L7"
            ]

            if len(diagonal_ray) % 2 == 1:
                enclosed_count += 1
                enclosed_area.add((i, j))

    # Visualize the result
    for (i, line) in enumerate(lines):
        colored_chars = []
        for (j, char) in enumerate(line):
            if (i, j) in pipe_set:
                colored_chars.append("\033[33m" + char + "\033[39m")
            elif (i, j) in enclosed_area:
                colored_chars.append("\033[32m" + char + "\033[39m")
            else:
                colored_chars.append("\033[34m" + char + "\033[39m")
        print("".join(colored_chars))

    print("Enclosed area: ", enclosed_count)


def read_graph(lines):
    nb_rows = len(lines)
    nb_cols = len(lines[0])

    graph = defaultdict(list)
    start_pos = None
    dots = []
    for (i, line) in enumerate(lines):
        for (j, char) in enumerate(line):
            match char:
                case "|":
                    handle_north(i=i, j=j, lines=lines, graph=graph)
                    handle_south(i=i, j=j, lines=lines, graph=graph)

                case "-":
                    handle_east(i=i, j=j, line=line, graph=graph)
                    handle_west(i=i, j=j, line=line, graph=graph)

                case "L":
                    handle_north(i=i, j=j, lines=lines, graph=graph)
                    handle_east(i=i, j=j, line=line, graph=graph)

                case "J":
                    handle_north(i=i, j=j, lines=lines, graph=graph)
                    handle_west(i=i, j=j, line=line, graph=graph)

                case "7":
                    handle_south(i=i, j=j, lines=lines, graph=graph)
                    handle_west(i=i, j=j, line=line, graph=graph)

                case "F":
                    handle_east(i=i, j=j, line=line, graph=graph)
                    handle_south(i=i, j=j, lines=lines, graph=graph)

                case "S":
                    start_pos = (i, j)
                    handle_north(i=i, j=j, lines=lines, graph=graph)
                    handle_south(i=i, j=j, lines=lines, graph=graph)
                    handle_east(i=i, j=j, line=line, graph=graph)
                    handle_west(i=i, j=j, line=line, graph=graph)

                case ".":
                    dots.append((i, j))

    assert start_pos
    return graph, start_pos, nb_rows, nb_cols


def handle_north(i, j, lines, graph):
    if i >= 1:
        upper_char = lines[i - 1][j]
        if upper_char in "|7FS":
            graph[(i, j)].append((i - 1, j))


def handle_east(i, j, line, graph):
    try:
        right_char = line[j + 1]
    except IndexError:
        pass
    else:
        if right_char in "-7JS":
            graph[(i, j)].append((i, j + 1))


def handle_south(i, j, lines, graph):
    try:
        south_char = lines[i + 1][j]
    except IndexError:
        pass
    else:
        if south_char in "SL|J":
            graph[(i, j)].append((i + 1, j))


def handle_west(i, j, line, graph):
    if j >= 1:
        west_char = line[j - 1]
        if west_char in "S-FL":
            graph[(i, j)].append((i, j - 1))


if __name__ == "__main__":
    init()
    part_one("../input.txt")
    part_two("../input.txt")
