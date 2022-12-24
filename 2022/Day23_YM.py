from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit
from collections import defaultdict
import itertools

# --------------------------------------------------------------------
# GET PUZZLE DATA FOR DAY 23›
# --------------------------------------------------------------------

data = get_data(day=23).splitlines()

# --------------------------------------------------------------------
# SIMULATE ELF'S PROCESS
# --------------------------------------------------------------------

DIRECTIONAL_OPERTIONS = (
    ((0, -1), (1, -1), (-1, -1)),  # NORTH
    ((0, 1), (1, 1), (-1, 1)),  # SOUTH
    ((-1, 0), (-1, 1), (-1, -1)),  # WEST
    ((1, 0), (1, 1), (1, -1)),  # EAST
)

grid = set()


def surrounding_neighbor(x_input, y_input):
    """RETURN TRUE IF TWO ELVES ARE PROPOSING SAME LOCATION, ELSE RETURN FALSE

    Args:
        x_input [int]: x coordinate of proposed space to move
        y_input [int]: y coordinate of proposed space to move

    Returns:
        [bool]: RETURNS TRUE IF SPACE IS PROPOSED BY TWO OR MORE ELVES
    """
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x == 0 and y == 0:
                continue
            if (x_input + x, y_input + y) in grid:
                return True
    return False


for y_pos, line in enumerate(data):
    for x_pos, position in enumerate(line):
        if position == "#":
            grid.add((x_pos, y_pos))

for i in itertools.count():
    proposed = defaultdict(list)
    new_grid = set()

    for x, y in grid:
        if surrounding_neighbor(x, y) == False:
            new_grid.add((x, y))

        for j in range(4):
            option = DIRECTIONAL_OPERTIONS[(i + j) % 4]
            if all((x + dx, y + dy) not in grid for dx, dy in option):
                dx, dy = option[0]
                proposed[x + dx, y + dy].append((x, y))
        else:
            new_grid.add((x, y))

    for pos, proposed_pos in proposed.items():
        if len(proposed_pos) == 1:
            new_grid.add(pos)
        else:
            new_grid.update(proposed_pos)

    grid = new_grid

    if i == 9:
        min_x = min(x for x, y in grid)
        max_x = max(x for x, y in grid)
        min_y = min(y for x, y in grid)
        max_y = max(y for x, y in grid)
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        print("Part 1:", width * height - len(grid))
        break
# --------------------------------------------------------------------
# SUBMIT PART 1
# --------------------------------------------------------------------

for i in range(1, 11):
    for j in range(4):
        print(DIRECTIONAL_OPERTIONS[(i + j) % 4])

DIRECTIONAL_OPERTIONS[2 % 4]
part1 = width * height - len(grid)
submit(part1, part="a")
