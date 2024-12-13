import os
from collections import defaultdict
from functools import partial, reduce
from math import gcd
from multiprocessing import Pool


def reduce_fraction(n, d):
    denominator = gcd(n, d)

    return n // denominator, d // denominator


def map_nodes(filename="./input.txt"):
    nodes = defaultdict(list)
    with open(filename, "r") as f:
        row = 0
        line = f.readline().strip()

        while line:
            for col, char in enumerate(line):
                if char != '.':
                    nodes[char].append((row, col))

            line = f.readline().strip()
            row += 1

    return nodes, row


def find_anti_nodes_for_pair(first, second, size):
    anti_nodes = set()

    locs = sorted([first, second], key=lambda p: (p[0], p[1]))
    first_x, first_y = locs.pop(0)
    second_x, second_y = locs.pop(0)

    x = second_x - first_x
    y = second_y - first_y

    first_anti_x = first_x - x
    first_anti_y = first_y - y
    if 0 <= first_anti_x < size and 0 <= first_anti_y < size:
        anti_nodes.add((first_anti_x, first_anti_y))

    second_anti_x = second_x + x
    second_anti_y = second_y + y
    if 0 <= second_anti_x < size and 0 <= second_anti_y < size:
        anti_nodes.add((second_anti_x, second_anti_y))

    return anti_nodes


def find_anti_nodes_for_pair_resonant(first, second, size):
    anti_nodes = set([first, second])

    locs = sorted([first, second], key=lambda p: (p[0], p[1]))
    first_x, first_y = locs.pop(0)
    second_x, second_y = locs.pop(0)

    dx = second_x - first_x
    dy = second_y - first_y
    dx, dy = reduce_fraction(dx, dy)

    first_x -= dx
    first_y -= dy
    while 0 <= first_x < size and 0 <= first_y < size:
        anti_nodes.add((first_x, first_y))

        first_x -= dx
        first_y -= dy

    second_x += dx
    second_y += dy
    while 0 <= second_x < size and 0 <= second_y < size:
        anti_nodes.add((second_x, second_y))

        second_x += dx
        second_y += dy

    return anti_nodes


def find_anti_nodes_for_node(locations, size, pair_fn):
    anti_nodes = set()
    for i in range(len(locations) - 1):
        for j in range(i + 1, len(locations)):
            anti_nodes |= pair_fn(locations[i], locations[j], size)

    return anti_nodes


def find_all_anti_nodes(nodes, size):
    finder_with_size = partial(find_anti_nodes_for_node, size=size, pair_fn=find_anti_nodes_for_pair)
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(finder_with_size, nodes.values())

    return len(reduce(set.union, results))


def find_all_anti_nodes_resonant(nodes, size):
    finder_with_size = partial(find_anti_nodes_for_node, size=size, pair_fn=find_anti_nodes_for_pair_resonant)
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(finder_with_size, nodes.values())

    return len(reduce(set.union, results))


if __name__ == "__main__":
    all_nodes, map_size = map_nodes()
    print(find_all_anti_nodes(all_nodes, map_size))
    print(find_all_anti_nodes_resonant(all_nodes, map_size))
