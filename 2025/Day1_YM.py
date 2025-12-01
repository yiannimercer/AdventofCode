# %% 
from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

# %% 
# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

data = get_data(day=1, year=2025).splitlines()

# %%

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

# Create a range of valid DIAL values (0-99)
DIAL = [x for x in range(100)]

# Set the starting position of the dial
DIAL_START = 50


def adjust_dial_position(position):
    """
    Adjust the dial when it goes out of bounds (0-99)
    
    e.g., if dial is at 95 and we turn it +10, it should wrap around to 5.
    """
    # Check how many times it makes a full circle so we can adjust accordingly
    full_circles = position // 100
    
    # If the position is greater than 99 or less than 0, adjust it accordingly
    if position > 99 or position < 0:
        # If position is greater than 99, subtract full circles * 100
        position -= (full_circles * 100)
    
    return position, full_circles

# %% 


# Initialize a variable to count how many times the positions lands on 0
answer_1 = 0

# Iterate through each instruction and adjust the dial accordingly
current_position = DIAL_START

# Iterate through each instruction and adjust the dial accordingly
for instruction in data:
    direction, amount = instruction[0], instruction[1:]
    amount = int(amount)
    
    # Apply the instruction to the current position
    if direction == "L":
        current_position -= amount
    elif direction == "R":
        current_position += amount
    
    # Adjust the dial position if it goes out of bounds
    current_position, _ = adjust_dial_position(current_position)
    
    # Count how many times the current position is 
    if current_position == 0:
        answer_1 += 1

# %% 

submit(answer_1, part="a", day=1, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 - COUNT ZERO PASSES MANUALLY
# ------------------------------------------------

# Start count at 0
answer_2 = 0

# Start position at 50
position = DIAL_START

# Iterate through each instruction and adjust the dial accordingly
for instruction in data:
    # Direction is positive for 'R' and negative for 'L'
    direction_factor, amount = 1 if instruction[0] == 'R' else -1, int(instruction[1:])
    
    # Flip the sign of 'L' instructions to negative
    amount = direction_factor * amount
    
    # Calculate quotient and remainder when dividing by +/-100
    quotient, n = divmod(amount, direction_factor * 100)
    
    # Add the quotient to the answer directly as that is how many full passes of 100 we make
    answer_2 += quotient
    
    # Now manually count each step in the remainder to see if we land on zero
    for i in range(abs(n)):
        position += direction_factor
        answer_2 += position % 100 == 0
    
# %%

submit(answer_2, part="b", day=1, year=2025)

# %%
