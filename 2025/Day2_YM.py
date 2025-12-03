# %% 
from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

# %% 
# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

data = get_data(day=2, year=2025).split(',')
sample = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124".split(',')

# %%

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------


# List to store the invalid IDs
invalid_ids = []

# Iterate through each range in the data
for range_pair in data:
    # Extract the start and end of the range
    range_start = int(range_pair.split('-')[0])
    range_end = int(range_pair.split('-')[1])
    # Iterate through each number in the range
    for i in range(range_start, range_end + 1):
        # Check the length of the integer ID
        string_length = len(str(i))
        # If the length of the ID number is divisible by 2, split it in half and compare
        if string_length % 2 == 0:
            first_half = str(i)[:string_length // 2]
            second_half = str(i)[string_length // 2:]
            # If the first half == second half, invalid ID
            if first_half == second_half:
                invalid_ids.append(int(i))
        
answer_a = sum(invalid_ids)

# %%

submit(answer_a, part="a", day=2, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------


def divisors(n: int):
    return [d for d in range(1, n + 1) if n % d == 0]


def chunk_str(s: str, n: int):
    """
    Split string s into chunks of size n
    
    e.g., chunk_str("123456789", 3) -> ["123", "456", "789"]
    """
    return [s[i:i + n] for i in range(0, len(s), n)]


def all_equal(lst: list):
    """
    Check if all elements in the list are equal
    """
    return all(x == lst[0] for x in lst)

invalid_ids = []

for range_pair in data:
    # Extract the start and end of the range
    range_start = int(range_pair.split('-')[0])
    range_end = int(range_pair.split('-')[1])
    # Iterate through each number in the range
    for i in range(range_start, range_end + 1):
        # Calculate proper divisors
        divisors_lst = divisors(len(str(i)))
        
        # Iterate through each divisor and break string into chunks (e.g., '123123' -> ['12', '31', '23'], ['123', '123'])
        for divisor in divisors_lst:
            chunks = chunk_str(str(i), divisor)
            
            if len(chunks) < 2:
                continue
            
            # If all chunks are equal, it's an invalid ID and add it and move to he next ID
            if all_equal(chunks):
                invalid_ids.append(int(i))
                break
        
        
# %%

answer_b = sum(invalid_ids)

# %%

submit(answer_b, part="b", day=2, year=2025)

# %%
