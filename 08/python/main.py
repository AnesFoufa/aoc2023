from itertools import cycle
from math import lcm


def part_one(path):
    graph, directions = read_graph_directions(path=path)
    position = "AAA"

    for (steps, direction) in enumerate(cycle(directions)):
        if position == "ZZZ":
            print(steps)
            break
        position = next_position(position=position, direction=direction, graph=graph)


def part_two(path):
    graph, directions = read_graph_directions(path=path)

    positions = [position for position in graph if position.endswith("A")]
    positions_steps = []

    for position in positions:
        for (steps, direction) in enumerate(cycle(directions)):
            if position.endswith("Z"):
                positions_steps.append(steps)
                break
            position = next_position(position, direction, graph)
    print(lcm(*positions_steps))


def read_graph_directions(path) -> tuple[dict[str, tuple[str, str]], str]:
    with open(path, "r") as f:
        file_lines = f.read().split("\n")
    directions = file_lines[0]

    graph = {}
    for line in file_lines[2:]:
        if not line.strip():
            continue
        start, directions_str = map(str.strip, line.split("="))
        right, left = map(
            str.strip, directions_str.removeprefix("(").removesuffix(")").split(",")
        )
        graph[start] = (right, left)

    return graph, directions


def next_position(
    position: str, direction: str, graph: dict[str, tuple[str, str]]
) -> str:
    if direction == "L":
        return graph[position][0]
    else:
        assert direction == "R"
        return graph[position][1]


if __name__ == "__main__":
    part_two("../example3.txt")
    part_two("../input.txt")
