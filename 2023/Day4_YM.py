from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

import re

#############
# READ DATA #
#############

data = get_data(day=4, year=2023).splitlines()
len(data)

##########
# PART 1 #
##########

def calculate_points(parsed_card_with_winnings):
    winning_numbers = parsed_card_with_winnings['winning_numbers']
    len_winning_numbers = len(winning_numbers)
    if len_winning_numbers == 0:
        points = 0  # Return 0 points if the list is empty
    else:
        points = 2 ** (len_winning_numbers - 1)
    parsed_card_with_winnings['points'] = points
    return parsed_card_with_winnings

def parse_card(card_string):
    # Splitting the string at '|'
    parts = card_string.split('|')

    # Extracting the card number using regex to handle varying spaces and formats
    card_num_match = re.search(r'Card\s+(\d+):', card_string)
    card_num = card_num_match.group(1) if card_num_match else 'Unknown'

    # Extracting and converting numbers to the left and right of '|' into lists of integers
    winning_nums = [int(num) for num in parts[0].split() if num.isdigit()]
    card_nums = [int(num) for num in parts[1].split() if num.isdigit()]

    # Creating a dictionary with the extracted information
    card_info = {
        'card_num': int(card_num),
        'winning_nums': winning_nums,
        'card_nums': card_nums
    }

    return card_info

def calculate_winner_nums(parsed_card):
    winner_nums = parsed_card['winning_nums']
    card_nums = parsed_card['card_nums']
    winning_numbers = list(set(winner_nums).intersection(card_nums))
    parsed_card['winning_numbers'] = winning_numbers
    return parsed_card


card_information = []

for card in data:
    parsed_card = parse_card(card)
    parsed_card_with_winners = calculate_winner_nums(parsed_card)
    parsed_card_with_points = calculate_points(parsed_card_with_winners)
    card_information.append(parsed_card_with_points)
    
all_points = []
for card_info in card_information:
    points = card_info['points']
    all_points.append(points)

part1_answer = sum(all_points)
submit(part1_answer, part='a', day=4, year=2023)

##########
# PART 2 #
##########

example_data = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
"Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]

parsed_cards = []

for card in data:
    parsed_card = parse_card(card)
    parsed_card_with_winners = calculate_winner_nums(parsed_card)
    parsed_cards.append(parsed_card_with_winners)

# Get the full set of cards, original and spawned
card_duplicates = {}

for parsed_card in parsed_cards:
    card_num = parsed_card['card_num']
    winning_numbers  = parsed_card['winning_numbers']
    # Add spawned cards for each original card
    if len(winning_numbers) > 0:
        visited = list(range(card_num + 1, card_num + len(winning_numbers) + 1))
        card_duplicates[card_num] = visited 
    else:
        card_duplicates[card_num] = []

total_cards = []
card_pile = list(card_duplicates.keys())  # Initialize card_pile with original cards

while card_pile:
    card = card_pile.pop()  # Remove the last card from the card pile
    total_cards.append(card)  # Add this card to the total_cards list
    card_pile.extend(card_duplicates.get(card, []))  # Add duplicated cards to the stack for each card num

part2_answer = len(total_cards)
submit(part2_answer, part='b', day=4, year=2023)




    