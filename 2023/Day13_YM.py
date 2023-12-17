from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------------------------
# READ DATA IN
# --------------------------------------------------------------------

notes = get_data(day=13, year=2023).splitlines()
grouped_notes = []
current_group = []

for note in notes:
    if note == '':
        if current_group:  # Check if the current group is not empty
            grouped_notes.append(current_group)
            current_group = []  # Reset for the next group
    else:
        current_group.append(note)

# Add the last group if it's not empty
if current_group:
    grouped_notes.append(current_group)
    
# Example
vertical_line_example = ['#.##..##.',
                         '..#.##.#.',
                         '##......#',
                         '##......#',
                         '..#.##.#.',
                         '..##..##.',
                         '#.#.##.#.']

horizontal_line_example = ['##..#.#..#..###',
  '##.#......#....',
  '####....#.#####',
  '.#.##.##.......',
  '#..#.#..####..#',
  '#..#.#..####..#',
  '.#.##.##.......']

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


def horizontal_check(pattern):
    n = len(pattern)
    for i in range(n - 1):
        # Check for two consecutive equal rows indicating potential line of symmetry
        if pattern[i] == pattern[i + 1]:
            # Check for symmetry
            symmetrical = True
            for j in range(1, i + 1):
                if i + j + 1 < n and pattern[i - j] != pattern[i + j + 1]:
                    symmetrical = False
                    break

            if symmetrical:
                # Return the count of lines above the line of symmetry, including it
                return i + 1

    return 0  # Return -1 if no symmetry is found


def vertical_check(pattern):
    """
    Similar check to the above, but first we transpose the pattern so we can identify a horizontal
    line of symmetry and then do the same check as above
    """
    transposed_pattern = [''.join(column) for column in zip(*pattern)]
    count_of_lines_above_symmetry_line = horizontal_check(transposed_pattern) if \
        isinstance(horizontal_check(transposed_pattern),int) else \
            "No Vertical Line of Symmetry"
    return count_of_lines_above_symmetry_line
    

lines_above_horizontal_symmetry_line = []
for pattern in grouped_notes:
    count_of_lines_above_symmetry_line = horizontal_check(pattern)
    lines_above_horizontal_symmetry_line.append(count_of_lines_above_symmetry_line)
    
lines_above_vertical_symmetry_line = []
for pattern in grouped_notes:
    count_of_lines_above_symmetry_line = vertical_check(pattern)
    lines_above_vertical_symmetry_line.append(count_of_lines_above_symmetry_line)


summarise_horizontal = [100 * line_count for line_count in lines_above_horizontal_symmetry_line]
part1_answer = sum(lines_above_vertical_symmetry_line) + sum(summarise_horizontal)

submit(part1_answer, part='a', day=13, year=2023)

#------------------------------------------------
# PART 2 
#------------------------------------------------

def flip_char(c):
    return '.' if c == '#' else '#'

def find_and_fix_smudge(pattern, check_function):
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            # Create a copy and flip the character at the current position
            modified_pattern = [list(line) for line in pattern]
            modified_pattern[row][col] = flip_char(modified_pattern[row][col])
            modified_pattern = [''.join(line) for line in modified_pattern]

            # Check for new line of reflection
            reflection_line = check_function(modified_pattern)
            if reflection_line > 0:
                return reflection_line
    return 0

def summarize_new_reflection_lines(grouped_notes):
    horizontal_summary = []
    vertical_summary = []

    for pattern in grouped_notes:
        horizontal_line = find_and_fix_smudge(pattern, horizontal_check)
        vertical_line = find_and_fix_smudge(pattern, vertical_check)

        horizontal_summary.append(100 * horizontal_line)
        vertical_summary.append(vertical_line)

    return sum(horizontal_summary) + sum(vertical_summary)

# Test with the provided examples
part2_answer = summarize_new_reflection_lines(grouped_notes)
print(part2_answer)

submit(part2_answer, part='b', day=13, year=2023)
