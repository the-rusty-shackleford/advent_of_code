class DiskChunk:
    def __init__(self, file_id, file_blocks, free_blocks):
        self.file_id = file_id
        self.file_blocks = file_blocks
        self.free_blocks = free_blocks

    def to_list(self):
        return [str(self.file_id)] * self.file_blocks + ["."] * self.free_blocks


def extract_input(filename="./input.txt"):
    with open(filename, "r") as f:
        return f.readline().strip()


def parse_disk_map(disk_map):
    parsed_disk_map = []
    last_id = None
    for i in range(0, len(disk_map)-1, 2):
        file_id = i // 2
        file_blocks = int(disk_map[i])
        free_blocks = int(disk_map[i+1])

        chunk = DiskChunk(file_id, file_blocks, free_blocks)
        parsed_disk_map += chunk.to_list()
        last_id = file_id

    chunk = DiskChunk(last_id + 1, int(disk_map[-1]), 0)
    parsed_disk_map += chunk.to_list()

    return parsed_disk_map


def rearrange_free_space(parsed_disk_map):
    rearranged = []

    lo, hi = 0, len(parsed_disk_map) - 1
    while lo <= hi:
        lo_char = parsed_disk_map[lo]

        if lo_char != '.':
            rearranged.append(lo_char)
            lo += 1
        else:
            while (hi_char := parsed_disk_map[hi]) == '.':
                hi -= 1
            rearranged.append(hi_char)
            lo += 1
            hi -= 1

    return rearranged


def checksum(rearranged_disk_map):
    check_sum = 0
    for i, num in enumerate(rearranged_disk_map):
        check_sum += i * int(num)

    return check_sum


if __name__ == "__main__":
    input_disk_map = extract_input()
    parsed_input_disk_map = parse_disk_map(input_disk_map)
    rearranged_input_disk_map = rearrange_free_space(parsed_input_disk_map)
    # print(rearranged_input_disk_map)
    print(checksum(rearranged_input_disk_map))
    # print(parse_disk_map("2333133121414131402"))
    # print(rearrange_free_space(parse_disk_map("2333133121414131402")))
    # print(checksum(rearrange_free_space(parse_disk_map("2333133121414131402"))))
