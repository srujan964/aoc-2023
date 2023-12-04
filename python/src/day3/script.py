import re
import string
import sys
from itertools import chain
from functools import reduce

if len(sys.argv) < 2:
    print("Usage: python script.pt input.txt")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, "r") as f:
    data = f.read().splitlines()

schematic = [row for row in data]
MAX_ROW = len(schematic)
MAX_COL = len(schematic[0])


class Neighbour:
    def __init__(self, value: str, pos: tuple):
        self.value = value
        self.row = pos[0]
        self.col = pos[1]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


class Part:
    def __init__(self, number: int, row: int, pos: tuple, neighbours: list):
        self.number = number
        self.row = row
        self.start = pos[0]
        self.end = pos[1]
        self.neighbours = neighbours

    def __eq__(self, other):
        return (
            self.number == other.number
            and self.start == other.row
            and self.end == other.col
        )

    def has_gear(self, gear: Neighbour):
        return gear in self.neighbours


def find_neighbours(positions: tuple) -> list:
    (row, columns) = positions
    adjacents = []
    c_start = columns[0] - 1 if columns[0] >= 1 else columns[0]
    c_end = columns[-1] + 1 if columns[-1] < MAX_COL - 1 else columns[-1]

    if row >= 1:
        adjacents.append([(row - 1, c) for c in range(c_start, c_end + 1)])

    if row < MAX_ROW - 1:
        adjacents.append([(row + 1, c) for c in range(c_start, c_end + 1)])

    adjacents.append([(row, c) for c in range(c_start, c_end + 1) if c not in columns])

    neighbouring_pos = list(chain(*adjacents))
    return [Neighbour(schematic[x][y], (x, y)) for x, y in neighbouring_pos]


parts = []

for i, row in enumerate(schematic):
    for match in re.finditer(r"(\d*)", row):
        if match.groups()[0]:
            number = int(match.groups(0)[0])
            neighbours = find_neighbours((i, range(match.start(), match.end())))

            if any(
                [x.value not in string.digits and x.value != "." for x in neighbours]
            ):
                parts.append(Part(number, i, (match.start(), match.end()), neighbours))


print(f"Result: {sum([part.number for part in parts])}")


def part_two():
    gears = []

    for i, row in enumerate(schematic):
        for match in re.finditer(r"(\*)", row):
            if match.groups(0)[0]:
                possible_gear = Neighbour("*", (i, match.start()))
                gears.append(possible_gear)

    gear_ratio_sum = 0
    for gear in gears:
        adjacent_parts = [part for part in parts if part.has_gear(gear)]
        if len(adjacent_parts) == 2:
            gear_ratio = reduce(lambda x, y: x.number * y.number, adjacent_parts)
            gear_ratio_sum += gear_ratio

    print(f"Gear ratio: {gear_ratio_sum}")


part_two()
