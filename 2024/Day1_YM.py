from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import numpy as np

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

# Load Data
data = get_data(day=1, year=2024).split('\n')

# Store left & right lists
left_list = []
right_list = []

# Iterate through data and store the location IDs from left and right to respective lists
for pair in data:
    pair_split = pair.split("   ")
    left_list.append(int(pair_split[0]))
    right_list.append(int(pair_split[1]))

# Iterate through and identify min values and calculate distance
distances = []
for i in range(len(left_list)):
    # Identify the min values in each list
    left_min = min(left_list)
    right_min = min(right_list)
    
    # Calcualte the abs distacne between the values
    distance = np.abs(left_min - right_min)
    
    # Append distance to list
    distances.append(distance)
    
    # Remove the min values identified
    left_list.remove(left_min)
    right_list.remove(right_min)

# Sum distances
answer_1 = sum(distances)

# Submit
submit(answer=answer_1, part='a', day=1, year=2024)

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------

# Reorganize data into left and right lists
data = get_data(day=1, year=2024).split('\n')

# Store left & right lists
left_list = []
right_list = []

# Iterate through data and store the location IDs from left and right to respective lists
for pair in data:
    pair_split = pair.split("   ")
    left_list.append(int(pair_split[0]))
    right_list.append(int(pair_split[1]))
    
# Iterate through, identify min from left list, count num of appearances in right_list and calculate similarity
similarity_scores = []
for i in range(len(left_list)):
    # Identify min of left list
    left_min = min(left_list)
    
    # Identify the num of times that min appears in the right list
    right_mode = right_list.count(left_min)
    
    # Calcualte similartiy score
    similarity_score = left_min * right_mode
    
    # Append similarity_score
    similarity_scores.append(similarity_score)
    
    # Delete min from the left_list
    left_list.remove(left_min)
    
# Sum similarity scores
answer_2 = sum(similarity_scores)

# Submit
submit(answer_2, part='b', day=1, year=2024)