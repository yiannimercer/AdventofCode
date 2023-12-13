from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()

import multiprocessing

# --------------------------------------------------------------------
# READ DATA
# --------------------------------------------------------------------

condition_records = get_data(day=12, year=2023).splitlines()

condition_records = [row.split(' ') for row in condition_records]

condition_records_formatted = []
for row in condition_records:
    springs = row[0]
    damage_size = tuple(int(x) for x in row[1].split(','))
    condition_records_formatted.append((springs, damage_size))
    
    
# # --------------------------------------------------------------------
# # PART 1
# # --------------------------------------------------------------------

def count_valid_arrangements(spring_str: str, in_nums: tuple[int], size=None) -> int:
    """
    Counts the number of ways to replace '?' in spring_str
    such that the sequence of '#' characters matches the counts in in_nums.
    Each number in in_nums represents a group of consecutive '#' characters.
    """
    if size is None:
        size = len(spring_str)

    # Base case: if no numbers left to process
    if not in_nums:
        return 1 if all(char in {".", "?"} for char in spring_str) else 0

    # Extract the current group size and the remaining groups
    current_group_size = in_nums[0]
    remaining_groups = in_nums[1:]

    # Calculate remaining space needed for the remaining groups
    space_needed_for_remaining = sum(remaining_groups) + len(remaining_groups)

    valid_arrangement_counts = 0
    # Iterate over possible positions for the current group
    for start_pos in range(size - space_needed_for_remaining - current_group_size + 1):
        # Construct a string with the current group of '#' characters
        pattern = "." * start_pos + "#" * current_group_size + "."
        # Check if the pattern fits in the current string without conflicts
        if all(existing_char in {expected_char, "?"} for existing_char, expected_char in zip(spring_str, pattern)):
            # Recursively count arrangements for the remaining part of the string and groups
            valid_arrangement_counts += count_valid_arrangements(spring_str[len(pattern):], remaining_groups, size - current_group_size - start_pos - 1)

    return valid_arrangement_counts

# valid_arrangement_counts = 0
# for i in range(len(condition_records_formatted)):
#     count = count_valid_arrangements(condition_records_formatted[i][0], condition_records_formatted[i][1])
#     valid_arrangement_counts += count
    
# submit(valid_arrangement_counts, part='a', day=12, year=2023)

#------------------------------------------------
# PART 2 
#------------------------------------------------

condition_records_formatted_expanded = [] 
for i in range(len(condition_records_formatted)):
    spring_str = condition_records_formatted[i][0]
    num_list = condition_records_formatted[i][1]
    condition_records_formatted_expanded.append((spring_str * 5, num_list * 5))

