from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

from collections import Counter

#------------------------------------------------
# READ DATA IN 
#------------------------------------------------

data = get_data(day=7, year=2023).splitlines()

#------------------------------------------------
# PART 1 
#------------------------------------------------

   
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


poker_hands = {}

for hand_bid in data:
    hand_bid = hand_bid.split()
    hand = hand_bid[0]
    bid = int(hand_bid[1])
    poker_hands[hand] = {'bid': bid, 'hand_type': None}
    
for hand in poker_hands:
    rank, hand_type = classify_hand(hand)
    poker_hands[hand]['hand_type'] = (rank, hand_type)

