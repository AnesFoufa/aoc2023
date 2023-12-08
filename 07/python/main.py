from dataclasses import dataclass
from enum import Enum
from collections import Counter


def part_one(path):
    solve(path=path, joker=False)


def part_two(path):
    solve(path=path, joker=True)


class Label(Enum):
    A = "A"
    K = "K"
    Q = "Q"
    J = "J"
    T = "T"
    Nine = "9"
    Eight = "8"
    Seven = "7"
    Six = "6"
    Five = "5"
    Four = "4"
    Three = "3"
    Two = "2"

    def __lt__(self, other):
        if self.value.isdigit():
            if other.value.isdigit():
                res = int(self.value) < int(other.value)
            else:
                res = True
        elif other.value.isdigit():
            res = False
        else:
            res = self.value + other.value in {
                "TJ",
                "TQ",
                "TK",
                "TA",
                "JQ",
                "JK",
                "JA",
                "QK",
                "QA",
                "KA",
            }
        return res

    def __repr__(self) -> str:
        return self.value


@dataclass
class LabelJoker:
    label: Label

    def __lt__(self, other: "LabelJoker"):
        if other.label == Label.J:
            return False
        elif self.label == Label.J:
            return True
        else:
            return self.label < other.label


class HandType(Enum):
    FiveOfKind = 7
    FourOfKind = 6
    FullHouse = 5
    ThreeOfKind = 4
    DoublePair = 3
    OnePair = 2
    HighCard = 1

    def __lt__(self, other: "HandType"):
        return self.value < other.value


@dataclass(order=True)
class Hand:
    type_: HandType
    labels: tuple[Label, Label, Label, Label, Label]

    @classmethod
    def from_labels(cls, labels: tuple[Label, Label, Label, Label, Label]):
        return Hand(type_=cls._compute_type_(labels), labels=labels)

    @classmethod
    def _compute_type_(cls, labels):
        counter = Counter(labels)
        most_common = counter.most_common()
        match most_common[0][1]:
            case 5:
                res = HandType.FiveOfKind
            case 4:
                res = HandType.FourOfKind
            case 3:
                count2 = most_common[1][1]
                if count2 == 2:
                    res = HandType.FullHouse
                else:
                    res = HandType.ThreeOfKind
            case 2:
                count2 = most_common[1][1]
                if count2 == 2:
                    res = HandType.DoublePair
                else:
                    res = HandType.OnePair
            case _:
                res = HandType.HighCard
        return res


@dataclass(order=True)
class HandJoker:
    type_: HandType
    labels: tuple[LabelJoker, LabelJoker, LabelJoker, LabelJoker, LabelJoker]

    @classmethod
    def from_hand(cls, hand: Hand):
        labels_joker = tuple(LabelJoker(label) for label in hand.labels)

        initial_hand_type = hand.type_
        count_of_j = len(
            [
                label_joker
                for label_joker in labels_joker
                if label_joker.label == Label.J
            ]
        )
        if count_of_j == 0:
            hand_type = initial_hand_type
        else:
            match initial_hand_type:
                case HandType.FiveOfKind | HandType.FourOfKind | HandType.FullHouse:
                    hand_type = HandType.FiveOfKind
                case HandType.ThreeOfKind:
                    hand_type = HandType.FourOfKind
                case HandType.DoublePair if count_of_j == 2:
                    hand_type = HandType.FourOfKind
                case HandType.DoublePair:
                    assert count_of_j == 1
                    hand_type = HandType.FullHouse
                case HandType.OnePair:
                    hand_type = HandType.ThreeOfKind
                case _:
                    hand_type = HandType.OnePair

        return HandJoker(type_=hand_type, labels=labels_joker)


def solve(path, joker):
    hands_bids = []

    with open(path, "r") as f:
        for line in f:
            hand_str, bid_str = line.split()
            labels = tuple(Label(char) for char in hand_str)
            hand = Hand.from_labels(labels)
            if joker:
                hand = HandJoker.from_hand(hand)
            bid = int(bid_str)
            hands_bids.append((hand, bid))

    hands_bids.sort(key=lambda x: x[0])

    res = sum(bid * (i + 1) for (i, (_, bid)) in enumerate(hands_bids))
    print(res)


if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
