import sys
import re
from functools import reduce

if len(sys.argv) < 2:
    print("Usage: python script.pt input.txt")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, "r") as f:
    data = f.read().splitlines()

limit = {"red": 12, "green": 13, "blue": 14}
possible_game_ids = []
powers = []


def record_instructions(entry: str):
    [game, details] = entry.split(":")
    [_, id] = game.split(" ")
    max_in_game = {}
    impossible = False
    for subset in details.split(";"):
        for pick in re.findall(r"(\d+\s[a-z]+),*", subset):
            [val, colour] = pick.split(" ")
            val = int(val)
            if int(val) > limit[colour]:
                impossible = True

            if colour not in max_in_game or (
                colour in max_in_game and val > max_in_game[colour]
            ):
                max_in_game[colour] = val
    power_of_set = reduce(lambda x, y: x * y, max_in_game.values())
    powers.append(power_of_set)
    if not impossible:
        possible_game_ids.append(int(id))


total_power = 0
for entry in data:
    record_instructions(entry)

print(f"Result: {sum(possible_game_ids)}")
print(f"Total power: {sum(powers)}")
