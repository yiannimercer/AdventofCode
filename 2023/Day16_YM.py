from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------
# READ DATA IN 
# ------------------------------------------------

contraption_raw = get_data(day=16, year=2023).splitlines()

example_input = ['.|...\\....',
                 '|.-.\\.....',
                 '.....|-...',
                 '........|.',
                 '..........',
                 '.........\\',
                 '..../.\\..',
                 '.-.-/..|..',
                 '.|....-|.\\',
                 '..//.|....']

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "R": (0, 1),
    "L": (0, -1),
}

next_direction = {
    ".": ["U", "R", "D", "L"],
    "/": ["R", "U", "L", "D"],
    "\\": ["L", "D", "R", "U"],
    "-": ["RL", "R", "RL", "L"],
    "|": ["U", "UD", "D", "UD"],
}


def is_in_bounding_box(coords, grid):
    return 0 <= coords[0] < len(grid) and 0 <= coords[1] < len(grid[0])


def add_tuples(tuple_1, tuple_2):
    if len(tuple_1) != len(tuple_2):
        return None
    else:
        return tuple(map(lambda i, j: i + j, tuple_1, tuple_2))


def get_next_coords(coords, grid):
    coords, heading = coords[:2], coords[2]
    new_headings = next_direction[grid[coords[0]][coords[1]]]["URDL".find(heading)]
    new_coords = []
    for new_heading in new_headings:
        new_coord = add_tuples(coords, directions[new_heading]) + (new_heading,)
        new_coords.append(new_coord)
    return new_coords


def get_energized_count(grid, start_heading):
    # For visited squares we keep track of both the coordinates and the heading, because
    # the same square with a different heading could result in a different path
    border, visited = set([start_heading]), set([start_heading])
    while len(border) > 0:
        new_border = set()
        for coords in border:
            for new_coords in get_next_coords(coords, grid):
                if is_in_bounding_box(new_coords[:2], grid) and new_coords not in visited:
                    new_border.add(new_coords)
                    visited.add(new_coords)
        border = new_border
    return len(set(map(lambda x: x[:2], visited)))

submit(get_energized_count(contraption_raw, (0, 0, "R")), part='a', day=16, year=2023)

# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------

n = len(contraption_raw) # The inputs are squares
energeized_count = 0
for i in range(n):
    for start in [(0, i, "S"), (n - 1, i, "N"), (i, n - 1, "W"), (i, 0, "E")]:
        count = get_energized_count(contraption_raw, start)
        energeized_count = max(energeized_count, count)
        
submit(energeized_count, part='b', day=16, year=2023)