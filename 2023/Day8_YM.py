from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

import re
from math import lcm
from functools import reduce


# ------------------------------------------------
# READ DATA IN
# ------------------------------------------------

data = get_data(day=8, year=2023).splitlines()

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------

# Organize & parse data
sequence = [*data[0]]
sequence_index = [0 if index == 'L' else 1 for index in sequence]
network = data[2:]
parsed_network = {m[0]: (m[1], m[2]) for node in network for m in re.findall(r"(\w{3}) = \((\w{3}), (\w{3})\)", node)}

# Set up initial parameters
sequence_self_index = 0
max_sequence_idx = len(sequence_index) - 1
current_id = 'AAA'
steps = 0

# Iterate through network map, indexing the network and sequence step list
while current_id != 'ZZZ':
    current_id = parsed_network[current_id][sequence_index[sequence_self_index]]
    steps += 1
    if max_sequence_idx == sequence_self_index:
        sequence_self_index = 0
    else:
        sequence_self_index += 1

submit(steps, part='a', day=8, year=2023)

# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------

keys_ending_in_a = {k:v for (k,v) in parsed_network.items() if k[-1] == 'A' in k}

sequence_self_index = 0
max_sequence_idx = len(sequence_index) - 1
current_id = None

step_counts = []
for current_id in keys_ending_in_a:
    steps = 0
    while current_id[-1] != 'Z':
        current_id = parsed_network[current_id][sequence_index[sequence_self_index]]
        steps += 1
        if max_sequence_idx == sequence_self_index:
            sequence_self_index = 0
        else:
            sequence_self_index += 1
    step_counts.append(steps)
    
part2_answer = reduce(lcm, step_counts)

submit(part2_answer, part='b', day=8, year=2023)
