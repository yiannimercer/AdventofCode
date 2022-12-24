from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit
import re

# --------------------------------------------------------------------
# DAY 22 PUZZLE DATA
# --------------------------------------------------------------------


data = get_data(day=22).split("\n\n")

# --------------------------------------------------------------------
# SOLVE DAY 22
# --------------------------------------------------------------------

# CREATE BOARD, ROW AND COLUMN ENDS,
board = {}
row_ends = {}
column_ends = {}
current = {}
facing = 0

row = 0
for inp in data[0].split("\n"):
    row += 1
    for num, value in enumerate(inp, 1):
        if value != " ":
            board[row, num] = True if value == "." else False
            if board.get((row - 1, num)) == None:
                column_ends[num] = (row, None)
            else:
                column_ends[num] = (column_ends[num][0], row)
            if not cur and row == 1:
                cur = (1, num)
            row_ends[row] = (row_ends.get(row, (num,))[0], num)

directions = tuple(re.findall("[0-9]+|[LR]", data[1]))

for dir in directions:
    if dir.isdigit():
        steps = int(dir)
        dp, di = not facing in (1, 3), (1, -1)[facing in (2, 3)]
        for _ in range(steps):
            new = cur[dp] + di
            ends = (column_ends, row_ends)[dp][cur[~dp]]
            if new < ends[0] or new > ends[1]:
                new = ends[0] if di == 1 else ends[1]
            if not board[(new_pos := (cur[~dp], new) if dp else (new, cur[~dp]))]:
                break
            cur = new_pos
    elif dir == "R":
        facing = (1, 2, 3, 0)[facing]
    else:
        facing = (3, 0, 1, 2)[facing]

cur
