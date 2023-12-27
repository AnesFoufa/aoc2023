from sys import argv
from dataclasses import dataclass
from operator import lt, gt
from typing import Any
from math import prod
from collections import deque
import portion as P

MAX_VALUE = 5000
MIN_VALUE = -1


@dataclass(frozen=True)
class Rating:
    x: int
    m: int
    a: int
    s: int

    def __iter__(self):
        yield self.x
        yield self.m
        yield self.a
        yield self.s


@dataclass(frozen=True)
class Condition:
    left_attribute: str
    operator: Any
    right_value: int

    def eval(self, rating: "Rating") -> bool:
        left_value: int = getattr(rating, self.left_attribute)
        return self.operator(left_value, self.right_value)

    def split(self, rating_range: "RatingRange") -> tuple["RatingRange", "RatingRange"]:
        interval: P.Interval = getattr(rating_range, self.left_attribute)
        match self.operator:
            case _ if self.operator is lt:
                interval1 = interval & P.closed(MIN_VALUE, self.right_value - 1)
                interval2 = interval & P.closed(self.right_value, MAX_VALUE)
            case _ if self.operator is gt:
                interval1 = interval & P.closed(self.right_value + 1, MAX_VALUE)
                interval2 = interval & P.closed(MIN_VALUE, self.right_value)
            case _:
                raise ValueError(self.operator)
        kwargs = {
            k: v
            for (k, v) in rating_range.__dict__.items()
            if k in "xmas" and k != self.left_attribute
        }
        kwargs[self.left_attribute] = interval1
        rating_range1 = RatingRange(**kwargs)
        kwargs[self.left_attribute] = interval2
        rating_range2 = RatingRange(**kwargs)
        return rating_range1, rating_range2


@dataclass(frozen=True)
class Rule:
    condition: Condition
    destination: str


@dataclass(frozen=True)
class RatingRange:
    x: P.Interval
    m: P.Interval
    a: P.Interval
    s: P.Interval

    def __len__(self):
        return prod(self._interval_length(i) for i in (self.x, self.m, self.a, self.s))

    @classmethod
    def empty(cls):
        return RatingRange(x=P.empty(), m=P.empty(), a=P.empty(), s=P.empty())

    @classmethod
    def _interval_length(cls, interval: P.Interval):
        if interval.atomic:
            return interval.upper - interval.lower + 1
        return sum(cls._interval_length(sub_interval) for sub_interval in interval)


Worflow = deque[Rule | str]


def part_one(path):
    workflows, ratings = read_workflows_ratings(path)
    sum_accepted_ratings = sum(
        sum(rating)
        for rating in ratings
        if accepted(workflows=workflows, destination="in", rating=rating)
    )
    print(sum_accepted_ratings)


def part_two(path):
    workflows, _ = read_workflows_ratings(path)
    rating_range = RatingRange(
        x=P.closed(1, 4000),
        m=P.closed(1, 4000),
        a=P.closed(1, 4000),
        s=P.closed(1, 4000),
    )
    ratings_worflows: deque[tuple[RatingRange, Worflow]] = deque(
        [(rating_range, deque(["in"]))]
    )
    accepted_ratings = []
    while ratings_worflows:
        accepted_range = scatter(ratings_worflows=ratings_worflows, workflows=workflows)
        if accepted_range != RatingRange.empty():
            accepted_ratings.append(accepted_range)
    print(sum(len(r) for r in accepted_ratings))


def read_workflows_ratings(path):
    with open(path, "r") as f:
        worflows_str, ratings_str = f.read().split("\n\n")
    workflows = parse_workflows(worflows_str)
    ratings = parse_ratings(ratings_str)
    return workflows, ratings


def accepted(workflows: dict[str, Worflow], destination: str, rating: Rating):
    while True:
        if destination == "A":
            return True
        if destination == "R":
            return False
        for rule_or_dest in workflows[destination]:
            match rule_or_dest:
                case Rule(condition=condition, destination=dest) if condition.eval(
                    rating
                ):
                    destination = dest
                    break
                case str(dest):
                    destination = dest
                    break
        else:
            raise ValueError((workflows, rating))


def scatter(
    ratings_worflows: deque[tuple[RatingRange, Worflow]], workflows: dict[str, Worflow]
) -> RatingRange:
    """
    Process the fiest RatingRange with the first step of its corresponding workflow.
    Updates the ratings and workflows and returns the accepted RatingRange
    """
    empty = RatingRange.empty()
    if not ratings_worflows:
        return empty
    rating_range, workflow = ratings_worflows.popleft()
    if not workflow:
        return empty
    rule_or_dest = workflow.popleft()
    match rule_or_dest:
        case "A":
            return rating_range
        case "R":
            return empty
        case str(dest):
            ratings_worflows.appendleft((rating_range, workflows[dest]))
            return empty
        case Rule(condition=condition, destination=destination):
            rating_range1, rating_range2 = condition.split(rating_range)
            ratings_worflows.appendleft((rating_range2, workflow))
            ratings_worflows.appendleft((rating_range1, deque([destination])))
            return empty


def parse_workflows(worflows_str: str):
    workflows: dict[str, Worflow] = dict()
    for workflow_line in worflows_str.split("\n"):
        workflow_line = workflow_line.strip()
        if not workflow_line:
            continue
        name, rules_str = workflow_line.split("{")
        assert rules_str[-1] == "}"
        workflows[name] = deque(
            [parse_rule(rule_str) for rule_str in rules_str[:-1].split(",")]
        )
    return workflows


def parse_ratings(ratings_str: str):
    res: list[Rating] = list()
    for rating_str in ratings_str.split("\n"):
        rating_str = rating_str.strip()
        if not rating_str:
            continue
        rating_str = rating_str.strip("{}")
        x_str, m_str, a_str, s_str = rating_str.split(",")
        x = int(x_str.split("=")[1])
        m = int(m_str.split("=")[1])
        a = int(a_str.split("=")[1])
        s = int(s_str.split("=")[1])
        res.append(Rating(x=x, m=m, a=a, s=s))
    return res


def parse_rule(rule_str: str):
    split_rule_str = rule_str.split(":")
    if len(split_rule_str) == 1:
        return split_rule_str[0]
    assert len(split_rule_str) == 2
    cond_str = split_rule_str[0]
    destination = split_rule_str[1]
    attribute = cond_str[0]
    match cond_str[1]:
        case ">":
            operator = gt
        case "<":
            operator = lt
        case _:
            raise ValueError(cond_str)
    right_value = int(cond_str[2:])
    condition = Condition(
        left_attribute=attribute, operator=operator, right_value=right_value
    )
    return Rule(condition=condition, destination=destination)


if __name__ == "__main__":
    path = argv[1]
    part_one(path)
    part_two(path)
