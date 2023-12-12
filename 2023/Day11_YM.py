from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()

import itertools
import math

# ------------------------------------------------
# READ DATA IN
# ------------------------------------------------

image = get_data(day=11, year=2023).splitlines()

# ------------------------------------------------
# PART 1
# ------------------------------------------------

# Expanding the Universe

def find_empty_space_indexes(image_input):
    # Finding empty rows
    empty_rows = [
        i for i, row in enumerate(image_input) if all(ch == "." for ch in row)
    ]

    # Finding empty columns
    empty_columns = []
    for j in range(len(image_input[0])):
        if all(image_input[i][j] == "." for i in range(len(image_input))):
            empty_columns.append(j)

    return empty_rows, empty_columns


empty_space_row_index, empty_space_column_index = find_empty_space_indexes(image)


def expand_universe(image_input, empty_rows, empty_columns):
    # Convert the string representation to a 2D list
    image_input = [list(row) for row in image_input]
    num_rows, num_cols = len(image_input), len(image_input[0])

    # Add new rows
    for i, row_idx in enumerate(empty_rows):
        # Adjust the index to account for already added rows
        adjusted_row_idx = row_idx + i + 1
        # Insert a new row of '.' characters
        image_input.insert(adjusted_row_idx, ['.' for _ in range(num_cols)])

    # Update the number of rows after adding new rows
    num_rows = len(image_input)

    # Add new columns
    for j, col_idx in enumerate(empty_columns):
        # Adjust the index to account for already added columns
        adjusted_col_idx = col_idx + j + 1
        for row in image_input:
            # Insert a '.' at the adjusted column index in each row
            row.insert(adjusted_col_idx, '.')

    return image_input

expanded_image = expand_universe(image, empty_space_row_index, empty_space_column_index)

def number_galaxies(expanded_image):
    galaxy_number = 1
    galaxy_numbers = []
    for i in range(len(expanded_image)):
        for j in range(len(expanded_image[i])):
            if expanded_image[i][j] == '#':
                expanded_image[i][j] = galaxy_number
                galaxy_numbers.append(galaxy_number)
                galaxy_number += 1
            else:
                continue
    return expanded_image, galaxy_numbers
            
expanded_image_numbered, unique_galaxies = number_galaxies(expanded_image)

def generate_unique_pairs(numbers_list):
    return list(itertools.combinations(numbers_list, 2))

galaxy_pairs = generate_unique_pairs(unique_galaxies)

def calculate_manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)

def generate_galaxy_coords(expanded_image_numbered):
    galaxy_coords = {}
    for y in range(len(expanded_image_numbered)):
        for x in range(len(expanded_image_numbered[y])):
            if expanded_image_numbered[y][x] in unique_galaxies:
                galaxy_coords[expanded_image_numbered[y][x]] = (y + 1, x + 1)
    return galaxy_coords

galaxy_coords = generate_galaxy_coords(expanded_image_numbered)

# Convert Galaxy Pairs to their Coordinates
galaxy_pair_coordinates = []
for galaxy_pair in galaxy_pairs:
    galaxy1, galaxy2 = galaxy_pair
    galaxy1_coord = galaxy_coords[galaxy1]
    galaxy2_coord = galaxy_coords[galaxy2]
    galaxy_pair_coordinates.append((galaxy1_coord,galaxy2_coord))
    
shortest_paths = []
for galaxy_pair_coords in galaxy_pair_coordinates:
    shortest_dist = calculate_manhattan_distance(galaxy_pair_coords[0], galaxy_pair_coords[1])
    shortest_paths.append(shortest_dist)

part1_answer = sum(shortest_paths)

submit(part1_answer, part='a', day=11, year=2023)

#------------------------------------------------
# PART 2 
#------------------------------------------------

image = get_data(day=11, year=2023).splitlines()

empty_space_row_index, empty_space_column_index = find_empty_space_indexes(image)

image = [list(row) for row in image]

expanded_image_numbered, unique_galaxies = number_galaxies(image)

galaxy_coords = generate_galaxy_coords(expanded_image_numbered)

galaxy_pairs = generate_unique_pairs(unique_galaxies)

# Convert Galaxy Pairs to their Coordinates
galaxy_pair_coordinates = []
for galaxy_pair in galaxy_pairs:
    galaxy1, galaxy2 = galaxy_pair
    galaxy1_coord = galaxy_coords[galaxy1]
    galaxy2_coord = galaxy_coords[galaxy2]
    galaxy_pair_coordinates.append((galaxy1_coord,galaxy2_coord))
    
empty_rows = [all(image[i][j] == '.' for j in range(m)) for i in range(n)]
empty_cols = [all(image[i][j] == '.' for i in range(n)) for j in range(m)]

def calculate_adjusted_manhattan_dist(a, b, expansion_factor=1000000):
    i1, j1 = a
    i2, j2 = b
    i1, i2 = min(i1, i2), max(i1, i2)
    j1, j2 = min(j1, j2), max(j1, j2)

    ans = 0
    for i in range(i1, i2):
        ans += 1
        if empty_rows[i]:
            ans += expansion_factor - 1
    for j in range(j1, j2):
        ans += 1
        if empty_cols[j]:
            ans += expansion_factor - 1

    return ans

# Update the loop to calculate the shortest paths with the adjusted distances
shortest_paths = []
for galaxy_pair_coords in galaxy_pair_coordinates:
    shortest_dist = calculate_adjusted_manhattan_dist(
        galaxy_pair_coords[0], 
        galaxy_pair_coords[1], 
        1000000
    )
    shortest_paths.append(shortest_dist)

part2_answer = sum(shortest_paths)

submit(part2_answer, part='b', day=11, year=2023)