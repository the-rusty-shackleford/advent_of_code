def extract_reports(filename="./input.txt"):
    with open(filename, "r") as f:
        data = [list(map(int, line.split())) for line in f]

    return data


def is_safe(report):
    first, second = int(report[0]), int(report[1])
    diff = first - second
    if diff == 0 or abs(diff) > 3:
        return False

    def is_same_direction_and_safe(num):
        return (num * diff > 0) and abs(num) <= 3

    for i in range(1, len(report)-1):
        first, second = int(report[i]), int(report[i+1])
        if not is_same_direction_and_safe(first - second):
            return False

    return True


def get_num_safe_reports(reports):
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe += 1

    return num_safe


def get_num_safe_enough_reports(reports):
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe += 1
            continue

        for i in range(len(report)):
            if is_safe(report[:i] + report[i+1:]):
                num_safe += 1
                break

    return num_safe


if __name__ == "__main__":
    aoc_reports = extract_reports()
    print(get_num_safe_reports(aoc_reports))
    print(get_num_safe_enough_reports(aoc_reports))

