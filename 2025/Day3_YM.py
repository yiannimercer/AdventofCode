# %% 
from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
from itertools import combinations


# %% 
# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

data = get_data(day=3, year=2025).splitlines()
sample = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111"
]

# %%

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

# Iterate through each bank and create a joltage tuple of the all possible ratings
max_joltage_ratings = []
for bank in data:
    possible_joltage_ratings = [int(str(x + y)) for x, y in combinations(bank, 2)]
    max_joltage_rating = max(possible_joltage_ratings)
    max_joltage_ratings.append(max_joltage_rating)
    
answer_1 = sum(max_joltage_ratings)
print(f"Answer 1: {answer_1}")

# %% 

submit(answer_1, part="a", day=3, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------

# List of max joltage ratings for each bank
max_joltage_ratings = []

# Target joltage rating
K = 12

for bank in data:
    # How many digits we're allowed to drop (length of the bank in the sample is 15, but 100 in the real data)
    to_remove = len(bank) - K  # This is statically 100 - 12 = 88 for the real data
    
    # Hold the chosen digits
    stack = []
    
    # Iterate through each digit in the bank
    for b in bank:
        # While we can still remove digits and the last chosen digit is smaller, pop it so we can add in the larger digit earlier
        while to_remove > 0 and stack and stack[-1] < b:
            stack.pop()
            to_remove -= 1
            
        # Add the current digit after popping smaller digits
        stack.append(b)
        # print(stack)
    
    # Join together the 12 digits 
    max_joltage_rating = ''.join(stack[:K])
    
    # Add the max joltage rating to the list
    max_joltage_ratings.append(int(max_joltage_rating))

answer_2 = sum(max_joltage_ratings)
print(f"Answer 2: {answer_2}")

# %%

submit(answer_2, part="b", day=3, year=2025)

# %%
