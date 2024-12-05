from copy import deepcopy
from collections import defaultdict, deque
import re


def extract_rules_in_degree_and_updates(filename="./input.txt"):
    with open(filename, "r") as f:
        line = f.readline()

        rules = defaultdict(set)
        rule_pattern = r"(\d+)\|(\d+)"
        
        in_degree = defaultdict(int)

        while line:
            rule_matches = [(int(match.group(1)), int(match.group(2))) for match in re.finditer(rule_pattern, line)]
            for k, v in rule_matches:
                rules[k].add(v)
                in_degree[v] += 1

            if line == "\n":
                updates = [list(map(int, raw_line.strip().split(","))) for raw_line in f.readlines()]

            line = f.readline()

    return rules, in_degree, updates


def walk_update(rules, update):
    visited = set()
    for page in update:
        for after in rules[page]:
            if after in visited:
                return visited
        visited.add(page)
    return visited


def validate_update(rules, update):
    return len(walk_update(rules, update)) == len(update)


def fix_update(rules, in_degree, update):
    copied_in_degree = deepcopy(in_degree)

    # prune in-degree map to allow localized topological sort
    for k, v in rules.items():
        if k not in update:
            for page in v:
                copied_in_degree[page] -= 1
            del copied_in_degree[k]

    queue = deque([node for node in copied_in_degree if not copied_in_degree[node]])
    fixed_update = []

    while queue:
        current = queue.popleft()
        fixed_update.append(current)
        for neighbor in rules[current]:
            copied_in_degree[neighbor] -= 1
            if not copied_in_degree[neighbor]:
                queue.append(neighbor)

    if set(fixed_update) != set(update):
        raise ValueError()

    return fixed_update


def process_updates(rules, updates):
    counter = 0

    for update in updates:
        if validate_update(rules, update):
            counter += int(update[len(update) // 2])

    return counter


def process_fixed_updates(rules, in_degree, updates):
    counter = 0

    for update in updates:
        if not validate_update(rules, update):
            fixed_update = fix_update(rules, in_degree, update)
            counter += int(fixed_update[len(fixed_update) // 2])

    return counter


if __name__ == "__main__":
    all_rules, actual_in_degree, all_updates = extract_rules_in_degree_and_updates()
    print(process_updates(all_rules, all_updates))
    print(process_fixed_updates(all_rules, actual_in_degree, all_updates))
