from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import re

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

data = get_data(day=3, year=2024)

# Define regex pattern
pattern = r'mul\(\d{1,3},\d{1,3}\)'

# Extract all matches using the above pattern
matches = re.findall(pattern, data)

# Iterate through the matches and extract the integers
matches_tuple = []
for match in matches:
    match_stripped = match.strip("mul")
    matches_tuple.append(eval(match_stripped))
    
# Calculate the sum of products 
answer_1 = sum((x * y) for x, y in matches_tuple)

# Submit
submit(answer=answer_1, part='a', day=3, year=2024)

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------

control_pattern = r"(don't\(\)|do\(\))"

# Split the string into segments based on control instructions
segments = re.split(control_pattern, data)

# Initialize variables
enabled = True  # Start with instructions enabled
valid_matches = []

# Process each segment
for segment in segments:
    # Check for control instructions
    if segment == "don't()":
        enabled = False
    elif segment == "do()":
        enabled = True
    elif enabled:
        # If enabled, extract valid mul instructions
        valid_matches.extend(re.findall(pattern, segment))
        
matches_tuple = []
for match in valid_matches:
    match_stripped = match.strip("mul")
    matches_tuple.append(eval(match_stripped))
    
# Calculate the sum of products 
answer_2 = sum((x * y) for x, y in matches_tuple)

# Submit
submit(answer=answer_2, part='b', day=3, year=2024)
