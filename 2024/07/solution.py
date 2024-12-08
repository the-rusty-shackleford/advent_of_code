import os
from multiprocessing import Pool


def parse_input(filename="./input.txt"):
    with open(filename, "r") as f:
        data = []
        for line in f.readlines():
            line = line.strip().split(":")
            data.append((int(line[0]), list(map(int, line[1].split()))))

    return data


def is_solvable(value, operands):
    n = len(operands)

    dp = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        dp[i][i].add(operands[i])

    for length in range(2, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for left_val in dp[i][k]:
                    for right_val in dp[k+1][j]:
                        dp[i][j].add(left_val + right_val)
                        dp[i][j].add(left_val * right_val)

    return value in dp[0][n-1]


def helper(equation):
    val, operands = equation
    solvable = is_solvable(val, operands)
    if solvable:
        return val
    return 0


def get_solvable_values(equations):
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(helper, equations)

    return results


def get_solvable_sum(equations):
    return sum(get_solvable_values(equations))


if __name__ == "__main__":
    lines = parse_input("input.txt")
    print(get_solvable_sum(lines))
