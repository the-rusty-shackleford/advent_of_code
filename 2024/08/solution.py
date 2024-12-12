import os
from collections import defaultdict
from functools import partial, reduce
from multiprocessing import Pool


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


def find_anti_nodes_for_node(locations, size):
    anti_nodes = set()
    for i in range(len(locations) - 1):
        for j in range(i + 1, len(locations)):
            locs = sorted([locations[i], locations[j]], key=lambda p: (p[0], p[1]))
            first_x, first_y = locs.pop(0)
            second_x, second_y = locs.pop(0)
            x = abs(first_x - second_x)
            y = abs(first_y - second_y)

            first_anti_x = first_x - x
            first_anti_y = first_y - y
            if 0 <= first_anti_x < size and 0 <= first_anti_y < size:
                anti_nodes.add((first_anti_x, first_anti_y))

            second_anti_x = second_x + x
            second_anti_y = second_y + y
            if 0 <= second_anti_x < size and 0 <= second_anti_y < size:
                anti_nodes.add((second_anti_x, second_anti_y))

    return anti_nodes


def find_all_anti_nodes(nodes, size):
    finder_with_size = partial(find_anti_nodes_for_node, size=size)
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(finder_with_size, nodes.values())

    print(results)
    print(reduce(set.union, results))

    return len(reduce(set.union, results))


if __name__ == "__main__":
    all_nodes, map_size = map_nodes("test_input.txt")
    # print(find_all_anti_nodes(all_nodes, map_size))
    for k, v in all_nodes.items():
        print(k)
        print(find_anti_nodes_for_node(v, map_size))
        print("** ** ** **")
