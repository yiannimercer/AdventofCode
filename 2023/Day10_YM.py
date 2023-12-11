from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

from collections import *
from enum import Enum

#------------------------------------------------
# READ DATA IN
#------------------------------------------------

grid = get_data(day=10, year=2023).splitlines()

#------------------------------------------------
# PART 1 
#------------------------------------------------

class DIRECTION(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
# calculates new coordinates from direction and current coordinates
def next_coordinates(coordinates, direction):
    y, x = coordinates
    if direction == DIRECTION.UP:
        return (y-1, x)  # Move up: decrease the y-coordinate
    if direction == DIRECTION.DOWN:
        return (y+1, x)  # Move down: increase the y-coordinate
    if direction == DIRECTION.LEFT:
        return (y, x-1)  # Move left: decrease the x-coordinate
    if direction == DIRECTION.RIGHT:
        return (y, x+1)  # Move right: increase the x-coordinate
    
# calculates new direction from pipe and current direction
def next_direction(pipe, direction):
    if pipe == '|':
        # If currently moving up, continue up; otherwise, continue down.
        return DIRECTION.UP if direction == DIRECTION.UP else DIRECTION.DOWN
    if pipe == '-':
        # If currently moving left, continue left; otherwise, continue right.
        return DIRECTION.LEFT if direction == DIRECTION.LEFT else DIRECTION.RIGHT
    if pipe == 'L':
        # If coming from down, turn right; otherwise, turn up.
        return DIRECTION.RIGHT if direction == DIRECTION.DOWN else DIRECTION.UP
    if pipe == 'J':
        # If coming from down, turn left; otherwise, turn up.
        return DIRECTION.LEFT if direction == DIRECTION.DOWN else DIRECTION.UP
    if pipe == '7':
        # If coming from up, turn left; otherwise, turn down.
        return DIRECTION.LEFT if direction == DIRECTION.UP else DIRECTION.DOWN
    if pipe == 'F':
        # If coming from up, turn right; otherwise, turn down.
        return DIRECTION.RIGHT if direction == DIRECTION.UP else DIRECTION.DOWN

visited = []

# find starting position of 'S'
start_x, start_y = next((x, y) for x, row in enumerate(grid) for y, val in enumerate(row) if val == 'S')
start = (start_x, start_y)
visited.append(start)
# find starting direction
y, x = start
direction = None

if y > 0:
    pipe = grid[y-1][x]
    if pipe == '|' or pipe == 'F' or pipe == '7':
        direction = DIRECTION.UP
if y < len(grid) - 1:
    pipe = grid[y+1][x]
    if pipe == '|' or pipe == 'J' or pipe == 'L':
        direction = DIRECTION.DOWN
if x > 0:
    pipe = grid[y][x-1]
    if pipe == '-' or pipe == 'F' or pipe == 'L':
        direction = DIRECTION.LEFT
if x < len(grid[0]) - 1:
    pipe = grid[y][x+1]
    if pipe == '-' or pipe == 'J' or pipe == '7':
        direction = DIRECTION.RIGHT

# take first step in direction
coords = next_coordinates(start, direction)
total_steps = 1

# go through all pipes until start is reached again and count the steps
while coords != start:
    visited.append(coords)
    y, x = coords
    pipe = grid[y][x]
    direction = next_direction(pipe, direction)
    coords = next_coordinates(coords, direction)
    total_steps += 1

part1_answer = total_steps//2

submit(total_steps, part='a', day=10, year=2023)

#------------------------------------------------
# PART 2 
#------------------------------------------------

# Initialize the grid_loop with the same dimensions as the original grid, filled with '.'
grid_loop = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]

# Fill in the traced loop coordinates with the corresponding pipe operators
for (y, x) in visited:
    grid_loop[y][x] = grid[y][x]  # Using the original grid to get the pipe character

# Displaying the grid_loop
for row in grid_loop:
    print(''.join(row))
    
grid_copy = [row[:] for row in grid_loop]
    
def flood_fill(grid, y, x):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]) or grid[y][x] != '.':
        return
    grid[y][x] = 'x'  # Mark the cell as filled
    flood_fill(grid, y+1, x)  # Down
    flood_fill(grid, y-1, x)  # Up
    flood_fill(grid, y, x+1)  # Right
    flood_fill(grid, y, x-1)  # Left

# Perform flood fill starting from the top-left corner
flood_fill(grid_copy, 0, 0)
flood_fill(grid_copy, len(grid_copy) - 1, len(grid_copy[0]) - 1)

# Displaying the grid_loop
for row in grid_copy:
    print(''.join(row))

# Count the remaining dots
enclosed_dots = sum(row.count('.') for row in grid_copy)

submit(enclosed_dots, part='b', day=10, year=2023)
