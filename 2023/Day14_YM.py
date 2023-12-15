from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------------------------
# READ DATA IN
# --------------------------------------------------------------------

platform = get_data(day=14, year=2023).splitlines()

example_platform = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....'
]

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


def roll_rocks_north(platform_input):
    matrix = [list(line) for line in platform_input]
    row_len, col_len = len(matrix), len(matrix[0])
    for col in range(col_len):
        # Iterate through each column and move the 0's up
        for row in range(row_len):
            if matrix[row][col] == "O":
                # Find the highest position this "0" can roll to before hitting a "#" or the top row
                new_row = row
                while new_row > 0 and matrix[new_row - 1][col] == ".":
                    new_row -= 1  # Moving up --> Index moving down
                # Move the "0" if it can go up
                if new_row != row:
                    matrix[new_row][col] = 'O'
                    matrix[row][col] = '.'
    return [''.join(row) for row in matrix]


def calculate_total_load(rolled_rocks_output):
    """
    Calculate the total load after rolling all rocks north
    """
    # Container to save the loads
    support_beam_loads = []
    # Get a list of the support beam line/row # (So index 0 is equivalent to the length of the entire list)
    support_beam_row_nums = list(range(1, len(rolled_rocks_output)+1))[::-1]
    # Iterate through each support beam
    for i in range(len(rolled_rocks_output)):
        # Count the number of rounded rocks ('O's)
        rolled_rocks_count = rolled_rocks_output[i].count('O')
        # Calculate the load on this support beam | Count of O's * Support Beam Number
        load = rolled_rocks_count * support_beam_row_nums[i]
        # Append the load value for that support beam to the container list
        support_beam_loads.append(load)
    # Return the same of the support beam load list
    return sum(support_beam_loads)


rolled_rocks = roll_rocks_north(platform)
total_load = calculate_total_load(rolled_rocks)

submit(total_load, part='a', day=14, year=2023)


# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------


def roll_rocks(platform_input, direction):
    matrix = [list(line) for line in platform_input]
    rows, cols = len(matrix), len(matrix[0])   
    if direction == 'N':
        for col in range(cols):
            for row in range(rows):
                if matrix[row][col] == 'O':
                    new_row = row
                    while new_row > 0 and matrix[new_row - 1][col] == '.':
                        new_row -= 1
                    if new_row != row:
                        matrix[new_row][col], matrix[row][col] = matrix[row][col], '.'

    elif direction == 'E':
        for row in matrix:
            for col in reversed(range(cols)):
                if row[col] == 'O':
                    new_col = col
                    while new_col < cols - 1 and row[new_col + 1] == '.':
                        new_col += 1
                    if new_col != col:
                        row[new_col], row[col] = row[col], '.'

    elif direction == 'S':
        for col in range(cols):
            for row in reversed(range(rows)):
                if matrix[row][col] == 'O':
                    new_row = row
                    while new_row < rows - 1 and matrix[new_row + 1][col] == '.':
                        new_row += 1
                    if new_row != row:
                        matrix[new_row][col], matrix[row][col] = matrix[row][col], '.'

    elif direction == 'W':
        for row in matrix:
            for col in range(cols):
                if row[col] == 'O':
                    new_col = col
                    while new_col > 0 and row[new_col - 1] == '.':
                        new_col -= 1
                    if new_col != col:
                        row[new_col], row[col] = row[col], '.'

    return [''.join(row) for row in matrix]


def execute_n_cycles(platform_input, N):
    """
    Helper function to execute the roll_rocks method N cycles       
    """
    roll_cycle = ['N', 'W', 'S', 'E']
    current_state = platform_input
    for _ in range(N):
        for direction in roll_cycle:
            current_state = roll_rocks(current_state, direction)
    return current_state


n_cycles = 1000000000
final_state = execute_n_cycles(example_platform, n_cycles)
    