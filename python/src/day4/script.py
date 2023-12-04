import sys
import re

if len(sys.argv) < 2:
    print("Usage: python script.pt input.txt")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, "r") as f:
    data = f.read().splitlines()


class WinningCard:
    def __init__(self, number: int, winning_numbers: list, quantity: int):
        self.number = number
        self.winning_numbers = winning_numbers
        self.quantity = quantity


total_points = 0
card_counts = []
copies = []
for card_no, card in enumerate(data, start=1):
    match = re.match(r"Card\s+\d+: ([\d+\s]+)\|([\d+\s]+)", card)
    if match:
        (winning_nums, card_nums) = tuple(
            map(
                lambda x: [int(n) for n in x.strip().split()],
                match.groups(),
            )
        )

        winning_nums_in_card = [num for num in card_nums if num in winning_nums]
        card_counts.append(WinningCard(card_no, winning_nums_in_card, 1))
        if len(winning_nums_in_card) > 0:
            points = 2 ** (len(winning_nums_in_card) - 1)
            total_points += points

cards_processed = 0
for card in card_counts:
    card_num = card.number
    winning_copies = list(range(card_num + 1, card_num + len(card.winning_numbers) + 1))
    for i in range(0, card.quantity):
        for copy in winning_copies:
            card_counts[copy - 1].quantity += 1

    cards_processed += card.quantity

print(f"Result:\n\nPart One: {total_points}\nPart Two: {cards_processed}")
