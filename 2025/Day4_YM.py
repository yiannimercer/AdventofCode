# %% 
from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
from utils.grid import Direction, Grid

# %% 
# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

data = get_data(day=4, year=2025).splitlines()
sample = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@."
]



# %%

# ------------------------------------------------
# PUZZLE 1 - COUNT NEIGHBORS
# ------------------------------------------------

# Initiate the puzzle input as a Grid
grid = Grid(data)

answer_a = 0
# Iterate through each cell in the grid
for row, col in grid.iter_positions():
    paper_roll = grid.get(row, col) == "@"
    if paper_roll:
        answer_a += 1 if grid.count_near(row, col, "@") < 4 else 0
        

# %%

submit(answer_a, part="a", day=4, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2 - DYNAMICALLY UPDATING GRID & RESCANNING
# ------------------------------------------------

# Initiate the puzzle input as a Grid
grid = Grid(data)

answer_b = 0

# Initialize with dummy value to enter the loop
movable_paper_rolls_coordinates = [(-1, -1)]

while len(movable_paper_rolls_coordinates) > 0:
    movable_paper_rolls_cnt = len(movable_paper_rolls_coordinates) if movable_paper_rolls_coordinates[0] != (-1, -1) else 0
    movable_paper_rolls_coordinates = []
    
    # Find positions of recently moved paper rolls & reset them to "."
    recently_moved = grid.find_all("X")
    grid.set_positions(recently_moved, ".")
    
    # Iterate through each cell in the grid
    for row, col in grid.iter_positions():
        paper_roll = grid.get(row, col) == "@"
        if paper_roll:
            movable = grid.count_near(row, col, "@") < 4
            if movable:
                movable_paper_rolls_coordinates.append((row, col))
                
    # Increment answer_b by the number of recently moved paper rolls
    answer_b += movable_paper_rolls_cnt
    
    # Mass replace movable paper rolls with "X"
    grid.set_positions(movable_paper_rolls_coordinates, "X")

    

# %%

submit(answer_b, part="b", day=4, year=2025)

# %%
