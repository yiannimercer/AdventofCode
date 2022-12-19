from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit
from collections import defaultdict
from itertools import product

# --------------------------------------------------------------------
# DAY 17 PUZZLE INPUT
# --------------------------------------------------------------------

jet_movements = get_data(day=17)

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


rock_shapes = [
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]],
    [[0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0]],
    [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 1, 0]],
    [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]],
]
G = defaultdict(int)


def rock_can_move(idx, x, y, dx, dy):
    x, y = x + dx, y + dy
    for r, c in product(range(4), repeat=2):
        if rock_shapes[idx][r][c]:
            tmp_x, tmp_y = x + c, y + (3 - r)
            if tmp_y <= 0 or tmp_x <= 0 or tmp_x > 7 or G[tmp_x, tmp_y]:
                return False
    return (x, y)


part_1, j_idx = 0, 0
for i in range(2022):
    x, y, ticks = 3, part_1 + 4, 0

    while True:
        if ticks % 2:
            if rock_can_move(i % len(rock_shapes), x, y, 0, -1):
                y -= 1
            else:
                break
        else:
            d = (1, 0) if jet_movements[j_idx % len(jet_movements)] == ">" else (-1, 0)
            res = rock_can_move(i % len(rock_shapes), x, y, *d)
            if res:
                x, y = res
            j_idx += 1
        ticks += 1

    for r, c in product(range(4), repeat=2):
        if rock_shapes[i % len(rock_shapes)][r][c]:
            tmp_x, tmp_y = x + c, y + (3 - r)
            G[tmp_x, tmp_y] = 1
            part_1 = max(part_1, tmp_y)

print(part_1)
# SUBMIT PART 1
submit(part_1, day=17, part="a")

# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------

part_2, j_idx = 0, 0
for i in range(1000000000000):
    x, y, ticks = 3, part_2 + 4, 0

    while True:
        if ticks % 2:
            if rock_can_move(i % len(rock_shapes), x, y, 0, -1):
                y -= 1
            else:
                break
        else:
            d = (1, 0) if jet_movements[j_idx % len(jet_movements)] == ">" else (-1, 0)
            res = rock_can_move(i % len(rock_shapes), x, y, *d)
            if res:
                x, y = res
            j_idx += 1
        ticks += 1

    for r, c in product(range(4), repeat=2):
        if rock_shapes[i % len(rock_shapes)][r][c]:
            tmp_x, tmp_y = x + c, y + (3 - r)
            G[tmp_x, tmp_y] = 1
            part_2 = max(part_2, tmp_y)

print(part_2)
