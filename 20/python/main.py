from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from pprint import PrettyPrinter
from math import lcm
from graphviz import Digraph

printer = PrettyPrinter(indent=3)


class Signal(Enum):
    high = "high"
    low = "low"


class Pulsable(ABC):
    @abstractmethod
    def pulse(self, origin: str, signal: Signal) -> list[tuple[str, Signal]]:
        pass


@dataclass()
class Broadcaster(Pulsable):
    destinations: list[str]

    def pulse(self, origin: str, signal: Signal) -> list[tuple[str, Signal]]:
        return [(d, signal) for d in self.destinations]


class FlipFlopState(Enum):
    on = "on"
    off = "off"

    @property
    def flip(self):
        if self == FlipFlopState.on:
            res = FlipFlopState.off
        else:
            assert self == FlipFlopState.off
            res = FlipFlopState.on
        return res


@dataclass()
class FlipFlop(Pulsable):
    destinations: list[str]
    state: FlipFlopState = FlipFlopState.off

    def pulse(self, origin: str, signal: Signal) -> list[tuple[str, Signal]]:
        if signal == Signal.high:
            res: list[tuple[str, Signal]] = []
        else:
            self.state = self.state.flip
            signal = Signal.high if self.state == FlipFlopState.on else Signal.low
            res = [(destination, signal) for destination in self.destinations]
        return res


@dataclass()
class Conjunction(Pulsable):
    origins: dict[str, Signal]
    destinations: list[str]

    def pulse(self, origin: str, signal: Signal) -> list[tuple[str, Signal]]:
        assert origin in self.origins
        self.origins[origin] = signal
        if all(
            received_signal == Signal.high for received_signal in self.origins.values()
        ):
            s = Signal.low
        else:
            s = Signal.high
        return [(destination, s) for destination in self.destinations]

    def add_origin(self, origin: str):
        self.origins[origin] = Signal.low


def part_one(path):
    predecessors, successors, module_types = read_graph(path)
    modules = build_modules(
        predecessors=predecessors, successors=successors, module_types=module_types
    )
    # printer.pprint(modules)
    nb_lows = 0
    nb_highs = 0
    for _ in range(1000):
        signals: deque[tuple[str, Signal, str]] = deque(
            [("button", Signal.low, "broadcaster")]
        )
        while signals:
            origin_name, signal, destination_name = signals.popleft()
            # print(f"{origin_name} -{signal.value}-> {destination_name}")
            if signal == Signal.low:
                nb_lows += 1
            else:
                nb_highs += 1
            if destination_name not in modules:
                continue
            destination = modules[destination_name]
            for new_destination, s in destination.pulse(
                origin=origin_name, signal=signal
            ):
                signals.append((destination_name, s, new_destination))
    print(nb_lows * nb_highs)


def part_two(input_path, output_path):
    predecessors, successors, module_types = read_graph(input_path)
    nodes = set(predecessors.keys()).union(set(successors.keys()))
    graph = build_graph(module_types=module_types, nodes=nodes, successors=successors)
    write_dot_file(output_path, digraph=graph)
    modules = build_modules(
        predecessors=predecessors, successors=successors, module_types=module_types
    )
    grandparents_of_output_module = [
        geandparent
        for parents in predecessors["rx"]
        for geandparent in predecessors[parents]
    ]
    periods = [
        subgraph_until_output(modules=modules, predecessors=predecessors, module=module)
        for module in grandparents_of_output_module
    ]
    print(lcm(*periods))


Predessors = dict[str, set[str]]
Successors = dict[str, list[str]]
ModuleTypes = dict[str, type[Pulsable]]
Modules = dict[str, Pulsable]


def read_graph(path):
    module_types: ModuleTypes = dict()
    successors: Successors = defaultdict(list)
    predecessors: Predessors = defaultdict(set)
    with open(path, "r") as f:
        for line in f:
            origin_str, destination_str = line.split(" -> ")
            origin_str = origin_str.strip()
            match origin_str[0]:
                case "%":
                    origin_name = origin_str[1:]
                    module_types[origin_name] = FlipFlop
                case "&":
                    origin_name = origin_str[1:]
                    module_types[origin_name] = Conjunction
                case _:
                    assert origin_str == "broadcaster", line
                    origin_name = origin_str
                    module_types[origin_str] = Broadcaster
            for destination in destination_str.split(","):
                destination_name = destination.strip()
                successors[origin_name].append(destination_name)
                predecessors[destination_name].add(origin_name)
    return predecessors, successors, module_types


def write_dot_file(path, digraph: Digraph):
    with open(path, "w") as f:
        f.write(digraph.source)


def build_modules(
    predecessors: dict[str, set[str]], successors: dict[str, list[str]], module_types
):
    modules: Modules = dict()
    for module_name, module_type in module_types.items():
        destinations = successors[module_name]
        match module_type:
            case _ if module_type is Broadcaster:
                modules[module_name] = Broadcaster(destinations=destinations)
            case _ if module_type is FlipFlop:
                modules[module_name] = FlipFlop(destinations=destinations)
            case _ if module_type is Conjunction:
                conjunction = Conjunction(origins=dict(), destinations=destinations)
                for predecessor_name in predecessors[module_name]:
                    conjunction.add_origin(predecessor_name)
                modules[module_name] = conjunction
    return modules


def subgraph_until_output(modules: Modules, predecessors: Predessors, module: str):
    node_parents = parents(module, predecessors=predecessors)
    jm_subgraph = {k: v for (k, v) in modules.items() if k in node_parents}
    return until_low_output(jm_subgraph, module)


def until_low_output(modules: Modules, output_module: str):
    res = 0
    while True:
        res += 1
        signals: deque[tuple[str, Signal, str]] = deque(
            [("button", Signal.low, "broadcaster")]
        )
        while signals:
            origin_name, signal, destination_name = signals.popleft()
            if destination_name == output_module and signal == Signal.low:
                return res
            if destination_name not in modules:
                continue
            destination = modules[destination_name]
            for new_destination, s in destination.pulse(
                origin=origin_name, signal=signal
            ):
                signals.append((destination_name, s, new_destination))


def parents(module: str, predecessors: Predessors):
    stack = [module]
    handled_nodes: set[str] = set()
    res: set[str] = set()
    while stack:
        node = stack.pop()
        handled_nodes.add(node)
        for pred in predecessors.get(node, []):
            res.add(pred)
            if pred not in handled_nodes:
                stack.append(pred)
    return res


def build_graph(module_types: ModuleTypes, nodes: set[str], successors: Successors):
    dot = Digraph()
    for node in nodes:
        match module_types.get(node):
            case t if t is Broadcaster:
                label = "broadcaster"
            case t if t is Conjunction:
                label = "conjunction"
            case t if t is FlipFlop:
                label = "flipflop"
            case _:
                label = "test"
        if node == "rx":
            label = "final"
        dot.node(name=node, label=label)
    for node, node_successors in successors.items():
        for node_successor in node_successors:
            if node in nodes and node_successor in nodes:
                dot.edge(head_name=node_successor, tail_name=node)
    return dot


if __name__ == "__main__":
    from sys import argv

    path = argv[1]
    output_path = argv[2]
    part_one(path)
    part_two(path, output_path)
