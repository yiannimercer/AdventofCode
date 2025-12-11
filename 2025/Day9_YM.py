# %% 
from dotenv import load_dotenv
from utils.grid import Grid
load_dotenv()
from aocd import get_data, submit
from itertools import combinations

# %% 

# ------------------------------------------------
# LOAD DATA 
# ------------------------------------------------

data = get_data(day=9, year=2025).splitlines()

sample = [
    '7,1',
    '11,1',
    '11,7',
    '9,7',
    '9,5',
    '2,5',
    '2,3',
    '7,3'
]
# sample = [tuple(line.split(',')) for line in sample]

# Initialzie a sample grid for visualization of sample data
sample_grid = Grid.from_dimensions(height=9, width=14, fill_char='.')

# Create coordinates for red squares
sample_red_square_coords = [(int(b), int(a)) for s in sample for a, b in [s.split(',')]]
red_square_coords = [(int(b), int(a)) for s in data for a, b in [s.split(',')]]

sample_grid.set_positions(sample_red_square_coords, '#')
print(sample_grid.draw())

def calculate_area(point1, point2):
    """Calculate the number of grid cells in a rectangle (inclusive)."""
    width = abs(point1[0] - point2[0]) + 1
    height = abs(point1[1] - point2[1]) + 1
    return width * height


# %% 

# ------------------------------------------------
# PUZZLE 1 - CALCULATE AREA
# ------------------------------------------------

# Generate the possible rectangles
possible_rectangles = list(combinations(red_square_coords, 2))

# Calculate the area for each rectangle
areas = {(rect[0], rect[1]): calculate_area(rect[0], rect[1]) for rect in possible_rectangles}

# Sort areas to find the largest
sorted_areas = dict(sorted(areas.items(), key=lambda item: item[1], reverse=True))

# Calculate area of largest rectangle
largest_rectangle = list(sorted_areas.items())[0]
print(f"Largest rectangle (sample): {largest_rectangle}")   

# Submit answer for puzzle 1
answer_a = largest_rectangle[1]
submit(answer_a, part='a', day=9, year=2025)

# %% 

# Draw the largest rectangle on the sample grid for visualization
# print(sample_grid.draw())
# print("\n")
# print("---------------------------------")
# print("\n")
# rectangle_positions = sample_grid.trace_rectangle(largest_rectangle[0][0], largest_rectangle[0][1], fill=True)
# sample_grid.set_positions(rectangle_positions, '#')
# print(sample_grid.draw())

# %%

# ------------------------------------------------
# PUZZLE 2 - PERIMETERS & AREAS (LARGEST RECTANGLE IN AREA)
# ------------------------------------------------

# # Generate the possible rectangles
# possible_rectangles = list(combinations(red_square_coords, 2))

# # Find max x & y coordinates to define grid size
# max_x = max([coord[0] for coord in red_square_coords])
# max_y = max([coord[1] for coord in red_square_coords])

# # Initialize a grid that is large enough to hold all coordinates
# grid = Grid.from_dimensions(height=max_y + 1, width=max_x + 1, fill_char='.')
# valid_area = grid.trace_polygon(red_square_coords, fill=False)  # Just work with perimeter coordinates

# # Calculate the area for each rectangle
# areas = {(rect[0], rect[1]): calculate_area(rect[0], rect[1]) for rect in possible_rectangles}

# # Sort areas to find the largest
# sorted_areas = dict(sorted(areas.items(), key=lambda item: item[1], reverse=True))


# # %% 

# # Iterate through the sorted rectangles starting with the largest area first
# for rectangle in sorted_areas.keys():
#     # Generate all the coordinates/positions the rectangle would cover
#     rectangle_positions = grid.trace_rectangle(rectangle[0], rectangle[1], fill=False)  # Just get the perimeter coordinates of the rectangle
    
#     # Check if any part of the rectangle perimeter is outside the valid area
#     rect_in_valid_area = sample_grid.is_within_shape(
#         positions=rectangle_positions,
#         shape=valid_area,
#         shape_is_filled=False,
#         positions_is_filled=False
#     )    
    
#     # Stop at the first valid rectangle found (which will be the largest)
#     if rect_in_valid_area:
#         largest_valid_rectangle = rectangle
#         break
    
# print(f"Largest valid rectangle: {largest_valid_rectangle}")
    
# # %% 

# # Submit answer for puzzle 2
# answer_b = sorted_areas[largest_valid_rectangle][1]
# submit(answer_b, part='b', day=9, year=2025)

# %%

# ------------------------------------------------
# PUZZLE 2: TRY AGAIN (THE GRID METHOD IS TOO COMPUTATIONALLY EXPENSIVE) 
# ------------------------------------------------

# Abstracting the grid methods to just work with coordinate sets
def trace_line(p1, p2):
    """Get all coordinates on a horizontal or vertical line."""
    r1, c1 = p1
    r2, c2 = p2
    positions = []
    
    if r1 == r2:
        for c in range(min(c1, c2), max(c1, c2) + 1):
            positions.append((r1, c))
    elif c1 == c2:
        for r in range(min(r1, r2), max(r1, r2) + 1):
            positions.append((r, c1))
    
    return positions


def trace_valid_perimeter(corners):
    """Get perimeter coordinates of a polygon"""
    perimeter = set()
    for i in range(len(corners)):
        p1 = corners[i]
        p2 = corners[(i + 1) % len(corners)]
        perimeter.update(trace_line(p1, p2))
    return perimeter


def get_rectangle_corners(p1, p2):
    """Get all 4 corners of rectangle, not entire perimeter."""
    r1, c1 = p1
    r2, c2 = p2
    r1, r2 = min(r1, r2), max(r1, r2)
    c1, c2 = min(c1, c2), max(c1, c2)
    
    return [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]

def is_inside_polygon(point, perimeter, max_x):
    """Check if point is inside polygon"""
    if point in perimeter:
        return True
    
    r, c = point
    crossings = 0
    for check_c in range(c + 1, max_x + 1):
        if (r, check_c) in perimeter:
            crossings += 1
    
    # If the point is inside the shape, it will only pass the perimeter once, otherwise it passes it twice
    return crossings % 2 == 1


def is_within_shape(positions, perimeter, max_x) -> bool:
    """Check if all positions are within shape. No grid needed."""
    return all(is_inside_polygon(pos, perimeter, max_x) for pos in positions)

# %% 


# Generate all possible rectangles to be made 
possible_rectangles = list(combinations(red_square_coords, 2))

# Find max_x coordinate to help with point-in-polygon checks
max_x = max(coord[1] for coord in red_square_coords)

# Get perimeter coordinates of the valid area polygon
valid_area_perimeter = trace_valid_perimeter(red_square_coords)

# Calculate the areas & sort each rectangle
areas = {(rect[0], rect[1]): calculate_area(rect[0], rect[1]) for rect in possible_rectangles}
sorted_areas = dict(sorted(areas.items(), key=lambda item: item[1], reverse=True))

# Iterate through the sorted rectangle by area
for rectangle in sorted_areas.keys():
    # Generate all the coordinates/positions the rectangle would cover
    rectangle_positions = trace_rectangle_perimeter(rectangle[0], rectangle[1])
    
    # Check if any part of the rectangle perimeter is outside the valid area
    rect_in_valid_area = is_within_shape(
        positions=rectangle_positions,
        perimeter=valid_area_perimeter,
        max_x=max_x
    )    
    
    # Stop at the first valid rectangle found (which will be the largest)
    if rect_in_valid_area:
        largest_valid_rectangle = rectangle
        break

# %%
