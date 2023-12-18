from dataclasses import dataclass
from heapq import heappush, heappop
from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @property
    def opposite(self):
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case Direction.LEFT:
                return Direction.RIGHT
            case _:
                return Direction.LEFT

    def __repr__(self) -> str:
        return self.value


@dataclass(frozen=True)
class LastDirections:
    direction: Direction | None
    len_chain: int
    min_consecutive: int
    max_consecutive: int

    def possible_directions(self):
        possible_directions = Direction
        opposite_last_direction = None
        if self.direction:
            opposite_last_direction = self.direction.opposite
            if self.len_chain < self.min_consecutive:
                possible_directions = [self.direction]
        forbidden_direction = None
        if self.len_chain == self.max_consecutive:
            forbidden_direction = self.direction
        for d in possible_directions:
            if d not in [forbidden_direction, opposite_last_direction]:
                yield d

    def add_direction(self, d: Direction):
        len_chain = 1 if d != self.direction else self.len_chain + 1
        return LastDirections(
            direction=d,
            len_chain=len_chain,
            min_consecutive=self.min_consecutive,
            max_consecutive=self.max_consecutive,
        )


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def move(self, direction: Direction):
        match direction:
            case Direction.UP:
                return self.move_along_y(-1)
            case Direction.DOWN:
                return self.move_along_y(1)
            case Direction.LEFT:
                return self.move_along_x(-1)
            case Direction.RIGHT:
                return self.move_along_x(1)
            case _:
                raise ValueError(direction)

    def move_along_x(self, delta: int) -> "Position":
        return Position(x=self.x + delta, y=self.y)

    def move_along_y(self, delta: int) -> "Position":
        return Position(x=self.x, y=self.y + delta)


@dataclass()
class Blocks:
    data: list[list[int]]

    def heat_loss(self, position: Position):
        return self.data[position.y][position.x]

    def __contains__(self, position: Position):
        return 0 <= position.y < self.nb_rows and 0 <= position.x < self.nb_cols

    @property
    def nb_cols(self):
        return len(self.data[0])

    @property
    def nb_rows(self):
        return len(self.data)


@dataclass(frozen=True)
class Crucible:
    position: Position
    last_directions: LastDirections

    def __lt__(self, other):
        return True


def part_one(path):
    solve(path, min_consecutive=0, max_consecutive=3)


def part_two(path):
    solve(path, min_consecutive=4, max_consecutive=10)


def solve(path, min_consecutive: int, max_consecutive: int):
    blocks = read_blocks(path=path)
    i, heat_losses = compute_heat_losses(
        blocks, min_consecutive=min_consecutive, max_consecutive=max_consecutive
    )
    last_position = Position(x=blocks.nb_cols - 1, y=blocks.nb_rows - 1)
    min_heat_loss = min(
        heat_loss
        for (crucible, heat_loss) in heat_losses.items()
        if crucible.position == last_position
    )
    print("min heat loss:", min_heat_loss)
    print(i, "iterations")


def read_blocks(path):
    with open(path, "r") as f:
        blocks_data = [[int(char) for char in line.strip()] for line in f]
    blocks = Blocks(blocks_data)
    return blocks


def compute_heat_losses(blocks: Blocks, min_consecutive: int, max_consecutive: int):
    initial_crucible = Crucible(
        position=Position(0, 0),
        last_directions=LastDirections(
            None, 0, min_consecutive=min_consecutive, max_consecutive=max_consecutive
        ),
    )
    heat_losses = {initial_crucible: 0}
    visited: set[Crucible] = set()
    queue: list[tuple[int, Crucible]] = [(0, initial_crucible)]
    i = 0
    while queue:
        i += 1
        heat_loss, current_crucible = heappop(queue)
        visited.add(current_crucible)
        for next_direction in current_crucible.last_directions.possible_directions():
            next_position = current_crucible.position.move(next_direction)
            if next_position in blocks:
                next_last_directions = current_crucible.last_directions.add_direction(
                    next_direction
                )
                next_crucible = Crucible(
                    position=next_position, last_directions=next_last_directions
                )
                if next_crucible not in visited:
                    next_heat_loss = heat_loss + blocks.heat_loss(next_position)
                    next_old_heat_loss = heat_losses.get(next_crucible)
                    if (
                        next_old_heat_loss is None
                        or next_old_heat_loss > next_heat_loss
                    ):
                        heappush(queue, (next_heat_loss, next_crucible))
                        heat_losses[next_crucible] = next_heat_loss
    return i, heat_losses


if __name__ == "__main__":
    part_one("../example.txt")
    part_two("../input.txt")
