def extract_lines(filename="./input.txt"):
    with open(filename, "r") as f:
        data = list(map(lambda x: x.strip("\n"), f.readlines()))

    return data


def count_xmas(data, word="XMAS"):
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]

    rows = len(data)
    columns = len(data)
    word_length = len(word)

    def matches(ro, col, d):
        x, y = d
        for i in range(word_length):
            r, c = ro + x * i, col + y * i

            if r < 0 or r >= rows or c < 0 or c >= columns or data[r][c] != word[i]:
                return False
        return True

    xmas = 0
    for row in range(rows):
        for column in range(columns):
            for direction in directions:
                if matches(row, column, direction):
                    xmas += 1

    return xmas


def count_x_mas(data, word="MAS"):
    directions = [
        [(-1, -1), (0, 0), (1, 1)],
        [(1, -1), (0, 0), (-1, 1)],
    ]
    reverse = list(map(lambda d: list(reversed(d)), directions))

    rows = len(data)
    columns = len(data[0])

    def matches(ro, col, d):
        for i, (x, y) in enumerate(d):
            r, c = ro + x, col + y

            if r < 0 or r >= rows or c < 0 or c >= columns or data[r][c] != word[i]:
                return False
        return True

    xmas = 0
    for row in range(rows):
        for column in range(columns):
            if sum(1 if matches(row, column, direction) else 0 for direction in directions + reverse) == 2:
                xmas += 1

    return xmas


if __name__ == "__main__":
    text = extract_lines()
    print(count_xmas(text))
    print(count_x_mas(text))
