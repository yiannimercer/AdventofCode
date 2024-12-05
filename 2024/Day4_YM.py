from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import re

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

data_grid = get_data(day=4, year=2024).splitlines()

# Define Directional Movement
directions = [
    (0, 1),  # Right
    (0, -1),  # Left
    (1, 0),  # Up
    (-1, 0),  # Down
    (1, 1),  # Down-Right Diagonal
    (1, -1),  # Down-Left Diagonal
    (-1, 1),  # Up-Right Diagonal
    (-1, -1)  # Up-Left Diagonal
]


def check_direction(grid, word, row_count, col_count, row, column, row_change, column_change):
    # Iterate through each character in the word:
    for i in range(len(word)):
        # Calculate the row and column for the i-th character in the direction (dr, dc)
        nr, nc = row + i * row_change, column + i * column_change
        
        # Check if the new position (nr, nc) is within the bounds of the grid
        if not (0 <= nr < row_count and 0 <= nc < col_count):  # If out of bounds
            return False  # The word cannot fit in this direction
        
        # Check if the character in the grid at (nr, nc) matches the i-th character of the word
        if grid[nr][nc] != word[i]:  # If there's a mismatch
            return False  # The word does not exist in this direction
        
    return True


row_count = len(data_grid)
col_count = len(data_grid[0])
seach_word = "XMAS"
count = 0

for r in range(row_count):
    for c in range(col_count):
        for rc, cc in directions:
            if check_direction(data_grid, seach_word, row_count, col_count, r, c, rc, cc):
                count += 1

answer_1 = count 

submit(answer=answer_1, part='a', day=4, year=2024)

# ------------------------------------------------
# PUZZLE 2 
# ------------------------------------------------


def is_x_shape(grid, row, column, row_count, col_count):
    # Check bounds to ensure diagnols exist
    if (
        row - 1 >= 0 and row + 1 < row_count and column - 1 >= 0 and column + 1 < col_count and
        grid[row][column] == 'A'  # Center must be 'A'
    ):
        
        # Check top-left & bottom-right diagonal (M and S)
        if (
            (grid[row - 1][column - 1] in {'M', 'S'} and grid[row + 1][column + 1] in {'M', 'S'}) and 
            grid[row - 1][column - 1] != grid[row + 1][column + 1]
        ):

            # Check top-right & bottom-left diagonal (M and S)
            if (
                (grid[row - 1][column + 1] in {'M', 'S'} and grid[row + 1][column - 1] in {'M', 'S'}) and 
                grid[row - 1][column + 1] != grid[row + 1][column - 1]
            ):
                return True
    return False


puzzle_2_count = 0
for row in range(len(data_grid)):
    for column in range(len(data_grid[0])):
        if is_x_shape(data_grid, row, column, len(data_grid), len(data_grid[0])):
            puzzle_2_count += 1
            
answer_2 = puzzle_2_count

submit(answer=answer_2, part='b', day=4, year=2024)


# ------------------------------------------------
# Scratch Work 
# ------------------------------------------------

grid = [
    ".M.S......",
    "..A..MSMS.",
    ".M.S.MAA..",
    "..A.ASMSM.",
    ".M.S.M....",
    "..........",
    "S.S.S.S.S.",
    ".A.A.A.A..",
    "M.M.M.M.M.",
    ".........."
]


count = 0
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if is_x_shape(grid, r, c, len(grid), len(grid[0])):
            count += 1
print(f"Example has {count} X's")