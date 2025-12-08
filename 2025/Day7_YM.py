# %% 
from dotenv import load_dotenv
from utils.grid import Grid, Direction
from collections import deque
load_dotenv()
from aocd import get_data, submit

# %%

# ------------------------------------------------
# GET DATA 
# ------------------------------------------------

data = get_data(day=7, year=2025).splitlines()
sample = [
    '.......S.......',
    '...............',
    '.......^.......',
    '...............',
    '......^.^......',
    '...............',
    '.....^.^.^.....',
    '...............',
    '....^.^...^....',
    '...............',
    '...^.^...^.^...',
    '...............',
    '..^...^.....^..',
    '...............',
    '.^.^.^.^.^...^.',
    '...............'
]

grid = Grid(data)


# %% 

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

# Find the entry point
entry_point = grid.find_first('S')

# Track visited positions 
visited = set()
active = deque([entry_point])

while active:
    row, col = active.popleft()
    
    # Trace downward until we hit a boundry or split 
    while grid.in_bounds(row, col):
        # print(active)
        if (row, col) in visited:
            break
        visited.add((row, col))
        current = grid.get(row, col)

        # Check for splitter
        if current == '^':
            # Add left and right traces 
            left = grid.move_if_valid(row, col, Direction.LEFT)
            right = grid.move_if_valid(row, col, Direction.RIGHT)
            
            if left and left not in visited:
                active.append(left)
            if right and right not in visited:
                active.append(right)
            break 
        
        # Move down
        row, col = grid.move(row, col, Direction.DOWN)

for r, c in visited:
    if grid.get(r, c) not in ('^', 'S'):
        grid.set(r, c, '|')


# %%

# Count the number of "|" characters 
answer_a = 0
for r, c in grid.find_all("^"):
    if grid.near(r, c)[Direction.UP].value == "|":
        answer_a += 1
    

# %%

submit(answer_a, part="a", day=7, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------

from collections import defaultdict

# Initialize our grid
grid = Grid(data)

# Dictionary that returns 0 for missing keys, tracks particle count per column
counts = defaultdict(int)

# Find the starting position (S) and set initial count to 1
start_row, start_col = grid.find_first('S')
counts[start_col] = 1

# Process each row from top to bottom
for row in range(grid.height):
    
    # Get all splitter positions in this row using iter_row
    splitters = [cell.col for cell in grid.iter_row(row) if cell.value == '^']
    
    # Skip rows with no splitters
    if not splitters:
        continue
    
    # Create fresh dict for next row's counts
    new_counts = defaultdict(int)
    
    # Process each column that currently has particles
    for col, count in counts.items():
        
        # If this column has a splitter, split the beam
        if col in splitters:
            
            # Send all particles left (adds to any existing count at col-1)
            new_counts[col - 1] += count
            
            # Send all particles right (adds to any existing count at col+1)
            new_counts[col + 1] += count
        
        # No splitter here, particles pass straight through
        else:
            new_counts[col] += count
    
    # Replace old counts with new counts for next iteration
    counts = new_counts

# Sum all particles that exited at the bottom
total = sum(counts.values())

print(f"Exit counts per column: {dict(sorted(counts.items()))}")
print(f"Total particles: {total}")
    
answer_b = total

# %%

submit(answer_b, part="b", day=7, year=2025)

# %%
