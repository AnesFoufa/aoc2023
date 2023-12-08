def part_one(path):
    sum_predicted_values = 0
    with open(path, "r") as f:
        for line in f:
            history = [int(word) for word in line.split()]
            sum_predicted_values += predict_next_value(history)

    print(sum_predicted_values)

def part_two(path):
    sum_predicted_values = 0
    with open(path, "r") as f:
        for line in f:
            history = [int(word) for word in line.split()]
            sum_predicted_values += predict_previous_value(history)

    print(sum_predicted_values)


def predict_next_value(history: list[int]) -> int:
    if len(set(history)) == 1:
        return history[-1]
    differences = []
    for i in range(len(history) - 1):
        differences.append(history[i + 1] - history[i])

    next_difference = predict_next_value(differences)
    return history[-1] + next_difference

def predict_previous_value(history: list[int]) -> int:
    if len(set(history)) == 1:
        return history[-1]
    differences = []
    for i in range(len(history) - 1):
        differences.append(history[i + 1] - history[i])

    previous_difference = predict_previous_value(differences)
    return history[0] - previous_difference

if __name__ == "__main__":
    part_one("../input.txt")
    part_two("../input.txt")
