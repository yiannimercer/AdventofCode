from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

import re

#############
# LOAD DATA #
#############

data = get_data(day=3, year=2023).splitlines()

special_characters = []
for line in data:
    for character in line:
        if character != '.' and character.isdigit() is False:
            special_characters.append(character)

##########
# PART 1 #
##########

def check_adjacent(data, special_chars):
    part_numbers = []

    for i, line in enumerate(data):
        digit_matches = re.finditer(r'(\d+)', line)

        for match in digit_matches:
            start_index, end_index = match.span()
            end_index -= 1  # Adjust end_index to point to the last digit

            # Initialize flags for special character adjacency
            special_char_adjacent = False

            # Left & Right Check
            if start_index > 0 and line[start_index - 1] in special_chars:
                special_char_adjacent = True
            if end_index < len(line) - 1 and line[end_index + 1] in special_chars:
                special_char_adjacent = True

            # Up & Down Check
            if i > 0 and any(data[i - 1][idx] in special_chars for idx in range(start_index, end_index + 1)):
                special_char_adjacent = True
            if i < len(data) - 1 and any(data[i + 1][idx] in special_chars for idx in range(start_index, end_index + 1)):
                special_char_adjacent = True

            # Diagonal Checks
            # Top-left and Top-right
            if i > 0:
                if start_index > 0 and data[i - 1][start_index - 1] in special_chars:
                    special_char_adjacent = True
                if end_index < len(line) - 1 and data[i - 1][end_index + 1] in special_chars:
                    special_char_adjacent = True

            # Bottom-left and Bottom-right
            if i < len(data) - 1:
                if start_index > 0 and data[i + 1][start_index - 1] in special_chars:
                    special_char_adjacent = True
                if end_index < len(line) - 1 and data[i + 1][end_index + 1] in special_chars:
                    special_char_adjacent = True

            # Add the number to part_numbers if a special character is adjacent
            if special_char_adjacent:
                part_numbers.append(match.group())

    return part_numbers
                    
                    
part_numbers = check_adjacent(data, special_characters)

part1_answer = sum([int(x) for x in part_numbers])
submit(part1_answer, part='a', day=3, year=2023)

##########  
# PART 2 #
##########

def find_adjacent_gears(data):
    number_positions = []
    row = 0
    for engine_line in data:
        column = 0
        mark = 0
        for character in engine_line:
            if character.isdigit():
                mark += 1
            elif mark > 0:
                current_number = engine_line[column - mark:column]
                number_positions.append([current_number, row, column - mark, column - 1, []])
                mark = 0
            else:
                mark = 0
            column += 1
        if mark > 0:
            current_number = engine_line[column - mark:column]
            number_positions.append([current_number, row, column - mark, column - 1, []])
        row += 1

    gears = {}
    for number in number_positions:
        for x in range(number[2] - 1, number[3] + 2):
            for y in range(number[1] - 1, number[1] + 2):
                if 0 <= x < len(data[0]) and 0 <= y < len(data) and data[y][x] == '*':
                    gear_key = str(1000 * y + x)
                    if gear_key in gears:
                        gears[gear_key].append(number[0])
                    else:
                        gears[gear_key] = [number[0]]

    adjacent_digit_pairs = []
    for gear in gears.values():
        if len(gear) >= 2:
            adjacent_digit_pairs.append(tuple(sorted(gear)[:2]))

    return adjacent_digit_pairs

gears = find_adjacent_gears(data)
gears_ratios = [int(gear[0]) * int(gear[1]) for gear in gears]
part2_answer = sum(gears_ratios)
submit(part2_answer, part='b', day=3, year=2023)

467 * 35
