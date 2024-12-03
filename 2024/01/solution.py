from typing import Tuple

from collections import defaultdict
import numpy as np


def extract_lists(filepath: str = "./input.txt") -> Tuple[np.array, np.array]:
    data = np.loadtxt(filepath)

    column1 = np.array(sorted(data[:, 0]))
    column2 = np.array(sorted(data[:, 1]))

    return column1, column2


def find_difference_sum(column1, column2):
    abs_differences = np.abs(column1 - column2)

    total_difference = np.sum(abs_differences)

    return total_difference


def find_similarity_score(column1, column2):
    d1 = defaultdict(int)
    d2 = defaultdict(int)

    for num in column1:
        d1[num] += 1

    for num in column2:
        d2[num] += 1

    total = 0
    for k, v in d1.items():
        total += k * v * d2[k]

    return total


if __name__ == "__main__":
    col1, col2 = extract_lists()
    print(find_difference_sum(col1, col2))
    print(find_similarity_score(col1, col2))
