import os
from collections import defaultdict
from copy import deepcopy
from multiprocessing import Pool


def parse_input(filename="./input.txt"):
    row_obstructions = defaultdict(list)
    col_obstructions = defaultdict(list)
    starting_position = (None, None)

    with open(filename, "r") as f:
        row_counter = 0
        line = f.readline().strip()

        while line:
            for col_counter, char in enumerate(line):
                if char == '^':
                    starting_position = (row_counter, col_counter)

                if char == '#':
                    row_obstructions[row_counter].append(True)
                    col_obstructions[col_counter].append(True)
                else:
                    row_obstructions[row_counter].append(False)
                    col_obstructions[col_counter].append(False)

            line = f.readline().strip()
            row_counter += 1

    return starting_position, row_obstructions, col_obstructions


def count_unique_visited_tiles(starting_position, row_obstructions, col_obstructions):
    visited = defaultdict(set)

    directions = [
        (-1, 0),  # up
        (0, 1),   # right
        (1, 0),   # down
        (0, -1)   # left
    ]

    def obs_directly_in_front(prow, pcol, pdir):
        x, y = directions[pdir % 4]
        if out_of_bounds(prow+x, pcol+y):
            return False
        return row_obstructions[prow+x][pcol+y]

    def out_of_bounds(prow, pcol):
        return prow < 0 or prow >= len(row_obstructions.keys()) or pcol < 0 or pcol >= len(col_obstructions.keys())

    direction = 0
    row, col = starting_position
    while True:
        if out_of_bounds(row, col):
            break

        visited[row].add(col)

        if obs_directly_in_front(row, col, direction):
            direction += 1
        else:
            r, c = directions[direction % 4]
            row += r
            col += c

    counter = 0
    for cols in visited.values():
        counter += len(cols)

    return counter


def does_loop(starting_position, row_obstructions, col_obstructions):
    visited = defaultdict(set)

    directions = [
        (-1, 0),  # up
        (0, 1),   # right
        (1, 0),   # down
        (0, -1)   # left
    ]

    def obs_directly_in_front(prow, pcol, pdir):
        x, y = directions[pdir % 4]
        if out_of_bounds(prow+x, pcol+y):
            return False
        return row_obstructions[prow+x][pcol+y]

    def out_of_bounds(prow, pcol):
        return prow < 0 or prow >= len(row_obstructions.keys()) or pcol < 0 or pcol >= len(col_obstructions.keys())

    direction = 0
    row, col = starting_position
    while True:
        if out_of_bounds(row, col):
            break

        if (col, direction % 4) in visited[row]:
            return True

        visited[row].add((col, direction % 4))

        if obs_directly_in_front(row, col, direction):
            direction += 1
        else:
            r, c = directions[direction % 4]
            row += r
            col += c

    return False


def sim_helper(row, col, starting_position, row_obstructions, col_obstructions):
    starting_row, starting_col = starting_position
    if (row, col) != starting_position and (row, col) != (starting_row-1, starting_col) and not row_obstructions[row][col]:
        copy_row_obstructions = deepcopy(row_obstructions)
        copy_col_obstructions = deepcopy(col_obstructions)
        copy_row_obstructions[row][col] = True
        copy_col_obstructions[col][row] = True
        return 1 if does_loop(starting_position, copy_row_obstructions, copy_col_obstructions) else 0

    return 0


def full_sim(starting_position, row_obstructions, col_obstructions):
    rows = len(row_obstructions.keys())
    cols = len(col_obstructions.keys())
    inputs = [(i, j, starting_position, row_obstructions, col_obstructions) for i in range(rows) for j in range(cols)]

    with Pool(processes=os.cpu_count()) as pool:
        results = pool.starmap(sim_helper, inputs)

    return sum(results)


if __name__ == "__main__":
    starting_pos, row_obs, col_obs = parse_input()
    print(count_unique_visited_tiles(starting_pos, row_obs, col_obs))
    print(full_sim(starting_pos, row_obs, col_obs))
