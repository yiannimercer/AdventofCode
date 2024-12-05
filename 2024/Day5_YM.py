from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

# Get Data
data = get_data(day=5, year=2024).splitlines()

# Separate the rules from the updates
rules = {rule for rule in data if "|" in rule} # Make it a set so it does a hash lookup (faster processing)
updates = [update for update in data if "|" not in update and "" != update]

# Cast the updates to a list of list (converting values to integers)

updates = [list(map(int, s.split(','))) for s in updates]


# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

# Count how many updates are in the right order already

valid_updates = []
invalid_updates = []
for i in range(len(updates)):
    updates_valid = True
    # Outer loop: Iterate over each value in the current list (updates[i]), except the last one
    for j in range(len(updates[i]) - 1):  # Exclude the last value
        for k in range(j + 1, len(updates[i])):  # Compare current value with subsequent values
            rule_to_check = f"{updates[i][j]}|{updates[i][k]}"  # Pair each value with those that follow
            if rule_to_check not in rules:
                updates_valid = False  # Mark as invalid
                break  # Exit inner loop
        if not updates_valid:
            invalid_updates.append(updates[i])  # Exit outer loop for this update list
    if updates_valid:  # If all checks passed
        valid_updates.append(updates[i])  # Add to valid updates
        
# Add up the middle value of each list (assuming they are all composed of an odd value length)

answer_1 = 0

for valid_update in valid_updates:
    middle_index = len(valid_update) // 2
    answer_1 += valid_update[middle_index]

submit(answer=answer_1, part='a', day=5, year=2024)

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------


# Redid part 1 sort of to make this step easier 
from collections import defaultdict

# Parse rules
needs = defaultdict(set)
needed_by = defaultdict(set)
for rule in rules:
    before, after = [int(e) for e in rule.split("|")]
    needs[after].add(before)
    needed_by[before].add(after)

# Validate updates
invalid_updates = []
for update in updates:
    valid = True
    seen = set()
    for page in update:
        if len(needs[page].intersection(update) - seen) > 0:
            valid = False
        seen.add(page)
    if not valid:
        invalid_updates.append(update)

# Fix invalid updates
fixed_updates = []
for update in invalid_updates:
    valid = []
    while len(valid) != len(update):
        for page in update:
            before = needs[page].intersection(update) - set(valid)
            if len(before) == 0 and page not in valid:
                valid.append(page)
    fixed_updates.append(valid)

answer_2 = 0

for valid_update in fixed_updates:
    middle_index = len(valid_update) // 2
    answer_2 += valid_update[middle_index]

submit(answer=answer_2, part='b', day=5, year=2024)