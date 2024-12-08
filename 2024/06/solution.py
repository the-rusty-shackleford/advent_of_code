from collections import defaultdict


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


if __name__ == "__main__":
    starting_pos, row_obs, col_obs = parse_input()
    print(count_unique_visited_tiles(starting_pos, row_obs, col_obs))
