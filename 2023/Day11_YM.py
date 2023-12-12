from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()


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
    num_rows, num_cols = len(image_input), len(image_input[0])
    
    # Add new rows
    


# Identify Pairs

# Calculate Shortest Distance Between Each Pair

# Calculate Sum of each Distance

# Submit Part 188765
