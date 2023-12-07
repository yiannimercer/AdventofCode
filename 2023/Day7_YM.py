import pandas as pd
from collections import Counter
from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()


# ------------------------------------------------
# READ DATA IN
# ------------------------------------------------

data = get_data(day=7, year=2023).splitlines()

# ------------------------------------------------
# PART 1
# ------------------------------------------------

# Classify Hand Function


def classify_hand(hand):
    # Count the frequency of each card
    card_count = {card: hand.count(card) for card in set(hand)}
    # Check for each hand type
    if 5 in card_count.values():
        return 1, "Five of a Kind"
    elif 4 in card_count.values():
        return 2, "Four of a Kind"
    elif 3 in card_count.values() and 2 in card_count.values():
        return 3, "Full House"
    elif 3 in card_count.values():
        return 4, "Three of a Kind"
    elif len([card for card in card_count.values() if card == 2]) == 2:
        return 5, "Two Pair"
    elif 2 in card_count.values():
        return 6, "One Pair"
    else:
        return 7, "High Card"


# Organize Data
poker_hands = []

for hand_bid in data:
    hand_bid = hand_bid.split()
    hand = hand_bid[0]
    bid = int(hand_bid[1])
    poker_hands.append({'hand': hand, 'bid': bid, 'hand_type': None})

# Classify Hands into Respective Type of Hands (e.g., Pairs, Full House, etc.)
poker_hands_classified = []

for hand in poker_hands:
    rank, hand_type = classify_hand(hand['hand'])
    hand.update({'hand_type': hand_type, 'hand_rank': rank})
    poker_hands_classified.append(hand)

# Assign Individual Card Ranking


def create_hand_card_ranking(hand):
    split_hand = [*hand['hand']]
    for i in range(len(split_hand)):
        if split_hand[i] in '23456789':
            hand[f'card{i+1}'] = int(split_hand[i])
        elif split_hand[i] == 'T':
            hand[f'card{i+1}'] = 10
        elif split_hand[i] == 'J':
            hand[f'card{i+1}'] = 11
        elif split_hand[i] == 'Q':
            hand[f'card{i+1}'] = 12
        elif split_hand[i] == 'K':
            hand[f'card{i+1}'] = 13
        elif split_hand[i] == 'A':
            hand[f'card{i+1}'] = 14


for hand in poker_hands_classified:
    create_hand_card_ranking(hand)

# Sort Hands by Level of Importance, Hand Type, First Card, Etc.
sorted_hands = sorted(poker_hands_classified, key=lambda k: (-k['hand_rank'],
                                                             k['card1'],
                                                             k['card2'],
                                                             k['card3'],
                                                             k['card4'],
                                                             k['card5']))

for i in range(len(sorted_hands)):
    sorted_hands[i]['total_rank'] = i + 1

winnings = []

for line in sorted_hands:
    bid = line['bid']
    total_rank = line['total_rank']
    winnings.append(bid * total_rank)

part1_answer = sum(winnings)

submit(part1_answer, part='a', day=7, year=2023)

# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------


def create_hand_card_ranking_jokers(hand):
    cards = [*hand['hand']]
    for i in range(len(cards)):
        if cards[i] in '23456789':
            hand[f'card{i+1}'] = int(cards[i])
        elif cards[i] == 'T':
            hand[f'card{i+1}'] = 10
        elif cards[i] == 'J':
            hand[f'card{i+1}'] = 1
        elif cards[i] == 'Q':
            hand[f'card{i+1}'] = 12
        elif cards[i] == 'K':
            hand[f'card{i+1}'] = 13
        elif cards[i] == 'A':
            hand[f'card{i+1}'] = 14


# Iterate through and classify the hand as if the 'J'
# ...card was a card that would return the highest ranking hand
for hand in poker_hands_classified:
    if "J" in hand['hand']:
        cards = hand['hand']
        split_cards = [*cards]
        non_joker_cards = list(set(split_cards))
        new_hand_info_list = []
        for i, char in enumerate(cards):
            for non_joker_card in ['2', '3', '4', '5', '6', '7', '8',
                                   '9', 'T', 'J', 'Q', 'K', 'A']:
                new_hand = cards[:i] + non_joker_card + cards[i+1:]
                new_hand_rank, new_hand_type = classify_hand(new_hand)
                new_hand_info = {'original_hand': cards,
                                 'new_hand': new_hand,
                                 'new_hand_rank': new_hand_rank,
                                 'new_hand_type': new_hand_type}
                new_hand_info_list.append(new_hand_info)
            for non_joker_card in ['2', '3', '4', '5', '6', '7', '8',
                                   '9', 'T', 'J', 'Q', 'K', 'A']:
                new_hand = cards.replace('J', non_joker_card)
                new_hand_rank, new_hand_type = classify_hand(new_hand)
                new_hand_info = {'original_hand': cards,
                                 'new_hand': new_hand,
                                 'new_hand_rank': new_hand_rank,
                                 'new_hand_type': new_hand_type}
                new_hand_info_list.append(new_hand_info)
        highest_rank_hand = min(
            new_hand_info_list, key=lambda x: x['new_hand_rank'])
        hand['new_hand'] = highest_rank_hand['new_hand']
        hand['new_hand_rank'] = highest_rank_hand['new_hand_rank']
        hand['new_hand_type'] = highest_rank_hand['new_hand_type']
    else:
        hand['new_hand'] = hand['hand']
        hand['new_hand_rank'] = hand['hand_rank']
        hand['new_hand_type'] = hand['hand_type']

# Rerank the individual cards so that J is ranked as the least
for hand in poker_hands_classified:
    create_hand_card_ranking_jokers(hand)

# Sort the hands by the new hand w/ wild cards and updated cards ranks (J = 1)    
sorted_hands_with_jokers = sorted(poker_hands_classified, key=lambda k: (-k['new_hand_rank'],
                                                             k['card1'],
                                                             k['card2'],
                                                             k['card3'],
                                                             k['card4'],
                                                             k['card5']))   

# Reassign rank
for i in range(len(sorted_hands_with_jokers)):
    sorted_hands_with_jokers[i]['total_rank'] = i + 1

# Calculate bid * rank and save to winnings list
winnings = []

for line in sorted_hands_with_jokers:
    bid = line['bid']
    total_rank = line['total_rank']
    winnings.append(bid * total_rank)

# Sum winnings and submit
part2_answer = sum(winnings)

submit(part2_answer, part='b', day=7, year=2023)