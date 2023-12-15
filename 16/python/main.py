from enum import Enum


class Tile(Enum):
    empty = "."
    vertical_splitter = "|"
    horizontal_splitter = "-"
    mirror = "/"
    back_mirror = "\\"


Contraption = list[list[Tile]]
Position = tuple[int, int]
Segment = tuple[Position, Position]


class Direction(Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"


Photon = tuple[Position, Direction]

Trajectory = list[Position]


def part_one(path):
    contraption = read_contraption(path)
    nb_energized_positions = compute_nb_energized_positions(
        contraption=contraption, initial_photon=((0, 0), Direction.right)
    )
    print(nb_energized_positions)


def part_two(path):
    contraption = read_contraption(path)
    nb_rows, nb_cols = len(contraption), len(contraption[0])
    initial_photons: list[Photon] = [((x, 0), Direction.down) for x in range(nb_cols)]
    initial_photons.extend([((0, y), Direction.right) for y in range(nb_rows)])

    initial_photons.extend([((x, nb_rows - 1), Direction.up) for x in range(nb_cols)])
    initial_photons.extend([((nb_cols - 1, y), Direction.left) for y in range(nb_rows)])

    print(
        max(
            compute_nb_energized_positions(contraption, photon)
            for photon in initial_photons
        )
    )


def compute_nb_energized_positions(contraption: Contraption, initial_photon: Photon):
    nb_rows = len(contraption)
    nb_cols = len(contraption[0])
    photons: list[Photon] = [initial_photon]
    energized_positions: set[Position] = set()
    added_segments: set[Segment] = set()
    while photons:
        (initial_position, direction) = photons.pop()
        trajectory = move_photon(
            contraption=contraption, photon=(initial_position, direction)
        )
        for position in trajectory:
            energized_positions.add(position)
        segment = (trajectory[0], trajectory[-1])
        if segment not in added_segments:
            x_final, y_final = trajectory[-1]
            tile_at_final_position = contraption[y_final][x_final]
            new_photons = next_photons(
                direction, (x_final, y_final), tile_at_final_position
            )
            for ((x, y), d) in new_photons:
                if 0 <= x < nb_cols and 0 <= y < nb_rows:
                    photons.append(((x, y), d))

            added_segments.add(segment)
    return len(energized_positions)


def read_contraption(path) -> Contraption:
    contraption: Contraption = []
    with open(path, "r") as f:
        for line in f:
            contraption.append([Tile(char) for char in line.strip()])
    return contraption


def move_photon(contraption: Contraption, photon: Photon) -> Trajectory:
    ((ix, iy), direction) = photon
    nb_rows, nb_cols = len(contraption), len(contraption[0])
    max_x = nb_cols - 1
    max_y = nb_rows - 1
    match direction:
        case Direction.right:
            final_position = (max_x, iy)
            blocking_tiles = {Tile.mirror, Tile.back_mirror, Tile.vertical_splitter}
        case Direction.down:
            final_position = (ix, max_y)
            blocking_tiles = {Tile.mirror, Tile.back_mirror, Tile.horizontal_splitter}
        case Direction.left:
            final_position = (0, iy)
            blocking_tiles = {Tile.mirror, Tile.back_mirror, Tile.vertical_splitter}
        case Direction.up:
            final_position = (ix, 0)
            blocking_tiles = {Tile.mirror, Tile.back_mirror, Tile.horizontal_splitter}
        case _:
            raise ValueError(direction)
    trajectory: Trajectory = []
    for x, y in gen_trajectory((ix, iy), final_position, direction):
        trajectory.append((x, y))
        if contraption[y][x] in blocking_tiles:
            break
    return trajectory


def gen_trajectory(
    initial_position: Position, final_position: Position, direction: Direction
):
    (ix, iy), (fx, fy) = (initial_position, final_position)
    match direction:
        case Direction.right:
            assert iy == fy
            assert fx >= ix
            for x in range(ix, fx + 1):
                yield (x, iy)
        case Direction.down:
            assert ix == fx
            assert fy >= iy
            for y in range(iy, fy + 1):
                yield (ix, y)
        case Direction.left:
            assert iy == fy
            assert fx <= ix
            for x in range(ix, fx - 1, -1):
                yield (x, iy)
        case Direction.up:
            assert ix == fx
            assert fy <= iy
            for y in range(iy, fy - 1, -1):
                yield (ix, y)
        case _:
            raise ValueError(direction)


def next_photons(
    direction: Direction, final_position: Position, tile_at_final_position: Tile
) -> list[Photon]:
    xf, yf = final_position
    match direction:
        case Direction.right:
            match tile_at_final_position:
                case Tile.vertical_splitter:
                    res: list[Photon] = [
                        (final_position, Direction.up),
                        (final_position, Direction.down),
                    ]
                case Tile.mirror:
                    res = [
                        ((xf, yf - 1), Direction.up),
                    ]
                case Tile.back_mirror:
                    res = [
                        ((xf, yf + 1), Direction.down),
                    ]
                case _:
                    res = [(final_position, direction)]
        case Direction.down:
            match tile_at_final_position:
                case Tile.horizontal_splitter:
                    res = [
                        (final_position, Direction.right),
                        (final_position, Direction.left),
                    ]
                case Tile.mirror:
                    res = [
                        ((xf - 1, yf), Direction.left),
                    ]
                case Tile.back_mirror:
                    res = [
                        ((xf + 1, yf), Direction.right),
                    ]
                case _:
                    res = [(final_position, direction)]
        case Direction.left:
            match tile_at_final_position:
                case Tile.vertical_splitter:
                    res = [
                        (final_position, Direction.up),
                        (final_position, Direction.down),
                    ]
                case Tile.mirror:
                    res = [
                        ((xf, yf + 1), Direction.down),
                    ]
                case Tile.back_mirror:
                    res = [
                        ((xf, yf - 1), Direction.up),
                    ]
                case _:
                    res = [(final_position, direction)]
        case Direction.up:
            match tile_at_final_position:
                case Tile.horizontal_splitter:
                    res = [
                        (final_position, Direction.right),
                        (final_position, Direction.left),
                    ]
                case Tile.mirror:
                    res = [
                        ((xf + 1, yf), Direction.right),
                    ]
                case Tile.back_mirror:
                    res = [
                        ((xf - 1, yf), Direction.left),
                    ]
                case _:
                    res = [(final_position, direction)]
        case _:
            raise ValueError(direction)

    return res


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
