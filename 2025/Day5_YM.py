# %% 
from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

# %%

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

data = get_data(day=5, year=2025).splitlines()

# Split the list into lists by the '' element in the list 
fresh_ingredients = [id_range for id_range in data if '-' in id_range]
available_ingredients = [id_range for id_range in data if '-' not in id_range and id_range != '']
    

sample_fresh = [
    '3-5',
    '10-14',
    '16-20',
    '12-18',
]

sample_available = [
    '1',
    '5',
    '8',
    '11',
    '17',
    '32'
]

# %% 

# ------------------------------------------------
# PUZZLE 1 - AVAILABLE & FRESH 
# ------------------------------------------------

answer_a = 0

# Create a range of fresh ingredient IDs
fresh_ingredients_ranges = [tuple(map(int, s.split('-'))) for s in fresh_ingredients]
fresh_ingredients_ranges = [range(x, y + 1) for x, y in fresh_ingredients_ranges]


# Iterate through each available ingredient ID & check if it is in any of the fresh ingredient ranges
for available_id in available_ingredients:
    available_id_fresh = any(int(available_id) in fresh_range for fresh_range in fresh_ingredients_ranges)
    if available_id_fresh:
        answer_a += 1

# %%

submit(answer_a, part="a", day=5, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 - ALL FRESH IDS (MERGE & PROCESS RANGES)
# ------------------------------------------------

# range1: |1--------10|
# ragne2:       |5--------15|
# merged: |1----------------15|

# Create a range of fresh ingredient IDs
fresh_ingredients_ranges = [tuple(map(int, s.split('-'))) for s in fresh_ingredients]
fresh_ingredients_ranges = [range(x, y + 1) for x, y in fresh_ingredients_ranges]


# Convert ranges to intervals
intervals = [(r.start, r.stop - 1) for r in fresh_ingredients_ranges]
# Sort by start
intervals.sort()

# Iterate through intervals and merge overlapping ones
merged = [intervals[0]]
for start, end in intervals:
    last_start, last_end = merged[-1]
    # Check if overlapping
    if start <= last_end + 1:
        merged[-1] = (last_start, max(last_end, end))
    else:
        merged.append((start, end))

# Iterate through the merged intervals and count total fresh IDs
answer_b = 0
for start, end in merged:
    answer_b += len(range(start, end + 1))



# %%

submit(answer_b, part="b", day=5, year=2025)

# %%
