from aocd import get_data, submit
from dotenv import load_dotenv
from heapq import *

load_dotenv()


# --------------------------------------------------------------------
# READ DATA IN
# --------------------------------------------------------------------

dig_plan = get_data(day=18, year=2023).splitlines()
example_dig_plan = ['R 6 (#70c710)',
                    'D 5 (#0dc571)',
                    'L 2 (#5713f0)',
                    'D 2 (#d2c081)',
                    'R 2 (#59c680)',
                    'D 2 (#411b91)',
                    'L 5 (#8ceee2)',
                    'U 2 (#caa173)',
                    'L 1 (#1b58a2)',
                    'U 2 (#caa171)',
                    'R 2 (#7807d2)',
                    'U 3 (#a77fa3)',
                    'L 2 (#015232)',
                    'U 2 (#7a21e3)']

# Format Data

dig_plan_dict = [{'direction': x[0], 'meters': x[1], 'color': x[2]} for x in [x.split(' ') for x in dig_plan]]

example_dig_plan_dict = [{'direction': x[0], 'meters': x[1], 'color': x[2]} for x in [x.split(' ') for x in example_dig_plan]]

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------

def generate_points_between(current_position, next_position):

    x1, y1 = current_position[0], current_position[1]
    x2, y2 = next_position[0], next_position[1]
    
    points = [current_position, next_position]

    # If the line is vertical
    if x1 == x2:
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            points.append((x1, y))

    # If the line is horizontal
    elif y1 == y2:
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            points.append((x, y1))
    
    return points

def generate_dig_points(dig_plan_dict):
    dig_points = [(0, 0)]    
    current_position = (0, 0)

    for movement in dig_plan_dict:
        movement_amount = int(movement['meters'])
        if movement['direction'] == 'L':
            next_position = (current_position[0] - movement_amount, current_position[1])
        elif movement['direction'] == 'R':
            next_position = (current_position[0] + movement_amount, current_position[1])
        elif movement['direction'] == 'U':
            next_position = (current_position[0], current_position[1] + movement_amount)
        else:
            next_position = (current_position[0], current_position[1] - movement_amount)
        inbetween_points = generate_points_between(current_position, next_position)
        current_position = next_position
        
        dig_points.extend(inbetween_points)
    return dig_points

    
def create_plane_with_marked_points(points):
    # Determine the size of the plane
    max_x = max(points, key=lambda p: p[0])[0]
    min_x = min(points, key=lambda p: p[0])[0]
    max_y = max(points, key=lambda p: p[1])[1]
    min_y = min(points, key=lambda p: p[1])[1]

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Create the plane with all points initialized to '.'
    plane = [['.' for _ in range(width)] for _ in range(height)]

    # Adjust points and mark them on the plane
    for x, y in points:
        adjusted_x = x - min_x
        adjusted_y = y - min_y
        plane[height - adjusted_y - 1][adjusted_x] = '#'

    return plane

def flood_fill_iterative(plane, x, y, fill_char):
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        # If the current position is out of bounds or not a '.', skip
        if x < 0 or x >= len(plane[0]) or y < 0 or y >= len(plane) or plane[y][x] != '.':
            continue

        # Fill the current position
        plane[y][x] = fill_char

        # Add adjacent positions to the stack
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

def fill_shape_iterative(plane):
    start_point = find_starting_point(plane)
    if start_point:
        flood_fill_iterative(plane, start_point[0], start_point[1], '#')


def find_starting_point(plane):
    for y in range(len(plane)):
        for x in range(len(plane[y])):
            if plane[y][x] == '.':
                return x, y
    return None

def print_plane(plane):
    for row in plane:
        print(' '.join(row))

        
dig_points = generate_dig_points(dig_plan_dict)  
plane = create_plane_with_marked_points(dig_points)
fill_shape_iterative(plane)
print_plane(plane)