import os
from functools import partial
from operator import add, mul, concat
from multiprocessing import Pool


def parse_input(filename="./input.txt"):
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().split(":")
            data.append((int(line[0]), list(map(int, line[1].split()))))

    return data


def is_solvable(value, operands, operators, values=None):
    new_operands = operands[:]
    if values is None:
        first = new_operands.pop(0)
        second = new_operands.pop(0)
        values = [op(first, second) for op in operators]

    if not new_operands:
        return value in values

    new_values = []
    second = new_operands.pop(0)
    while values:
        first = values.pop(0)
        new_values.extend([op(first, second) for op in operators])

    return is_solvable(value, new_operands, operators, new_values)


def helper(equation, operators):
    val, operands = equation
    solvable = is_solvable(val, operands, operators)
    if solvable:
        return val
    return 0


def get_solvable_values(equations, operators):
    helper_with_operators = partial(helper, operators=operators)
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(helper_with_operators, equations)

    return results


def custom_concat(first, second):
    return int(concat(str(first), str(second)))


def get_solvable_sum(equations, operators):
    return sum(get_solvable_values(equations, operators))


if __name__ == "__main__":
    lines = parse_input("input.txt")
    print(get_solvable_sum(lines, [add, mul]))
    print(get_solvable_sum(lines, [add, mul, custom_concat]))
