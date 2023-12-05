import portion as P
from typing import Tuple


def part_one(path):
    with open(path, "r") as f:
        file_blocks = f.read().split("\n\n")

    seeds = [int(seed_str) for seed_str in file_blocks[0].split(":")[1].split()]

    intervals = []
    for block in file_blocks[1:]:
        current_interval = []
        for line in block.split("\n")[1:]:
            if not line.strip():
                continue
            dest_low, orig_low, rng = map(int, line.split())
            current_interval.append((orig_low, orig_low + rng - 1, dest_low - orig_low))
        current_interval.sort()
        intervals.append(current_interval)

    min_location = None
    for seed in seeds:
        location = seed
        for interval in intervals:
            for (low, high, translation) in interval:
                if location < low:
                    break
                if location <= high:
                    location += translation
                    break
        if min_location is None or min_location > location:
            min_location = location
    print(min_location)


def part_two(path):
    with open(path, "r") as f:
        file_blocks = f.read().split("\n\n")

    seeds_interval: P.Interval = P.empty()
    seeds_strs = file_blocks[0].split(":")[1].split()
    for i in range(0, len(seeds_strs), 2):
        low = int(seeds_strs[i])
        high = low + int(seeds_strs[i + 1]) - 1
        seeds_interval: P.Interval = seeds_interval | P.closed(low, high)

    intervals_translations_list: list[list[Tuple[P.Interval, int]]] = []
    unions_of_intervals: list[P.Interval] = []
    for block in file_blocks[1:]:
        current_union_of_intervals = P.empty()
        current_intervals_translations = []
        for line in block.split("\n")[1:]:
            if not line.strip():
                continue
            dest_low, orig_low, rng = map(int, line.split())
            origin_interval = P.closed(orig_low, orig_low + rng - 1)
            current_union_of_intervals = current_union_of_intervals | origin_interval
            current_intervals_translations.append(
                (origin_interval, dest_low - orig_low)
            )
        intervals_translations_list.append(current_intervals_translations)
        unions_of_intervals.append(current_union_of_intervals)

    locations_interval = seeds_interval
    for (union_of_intervals, intervals_translations) in zip(
        unions_of_intervals, intervals_translations_list
    ):
        diff = locations_interval - union_of_intervals
        translated_intervals = P.empty()
        for (interval, translation) in intervals_translations:
            translated_intervals = translated_intervals | translate_interval(
                locations_interval & interval, translation
            )
        locations_interval = diff | translated_intervals

    print(locations_interval.lower)


def translate_interval(interval, translation):
    def translate_bound(bound):
        return bound + translation

    return interval.apply(
        lambda x: x.replace(upper=translate_bound, lower=translate_bound)
    )


if __name__ == "__main__":
    part_two("../input.txt")
