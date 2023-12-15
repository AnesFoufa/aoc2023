from collections import OrderedDict


def part_one(path):
    steps = read_steps(path=path)
    res = sum(hashmap(step) for step in steps)
    print(res)


Step = str
Label = str
FocalLength = int
Box = OrderedDict[Label, FocalLength]


def part_two(path):
    steps = read_steps(path=path)
    boxes: list[Box] = [OrderedDict() for _ in range(256)]

    for step in steps:
        if step.endswith("-"):
            label = step[:-1]
            i_box = hashmap(label)
            box = boxes[i_box]
            box.pop(label, 0)
        else:
            label, focal_length_str = step.split("=")
            focal_length = int(focal_length_str)
            i_box = hashmap(label)
            box = boxes[i_box]
            box[label] = focal_length

    for (i_box, box) in enumerate(boxes, 1):
        for (i_label, (label, length)) in enumerate(box.items(), 1):
            res += i_label * i_box * length
    print(res)


def read_steps(path):
    with open(path, "r") as f:
        init_sequence = f.read().strip()
    return init_sequence.split(",")


def hashmap(step: str) -> int:
    val = 0
    for char in step:
        val = ((val + ord(char)) * 17) % 256
    return val


if __name__ == "__main__":
    part_one(path="../input.txt")
    part_two(path="../input.txt")
