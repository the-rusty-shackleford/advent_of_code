import re as regex


def extract_command_text(filename="./input.txt"):
    with open(filename, "r") as f:
        data = f.read()

    return data


def extract_mul_commands(data):
    pattern = r"mul\((\d+),(\d+)\)"
    return regex.findall(pattern, data)


def splice_dont_commands(data):
    pattern = r"([\s\S]*?)(don't\(\)[\s\S]*?do\(\))([\s\S]*?)"
    return regex.sub(pattern, r"\1\3", data)


def parse_mul_commands(commands):
    total = 0
    for (n1, n2) in commands:
        total += int(n1) * int(n2)

    return total


if __name__ == "__main__":
    text = extract_command_text()
    mul_commands = extract_mul_commands(text)
    print(parse_mul_commands(mul_commands))
    spliced_text = splice_dont_commands(text)
    spliced_mul_commands = extract_mul_commands(spliced_text)
    print(parse_mul_commands(spliced_mul_commands))
