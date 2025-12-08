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

