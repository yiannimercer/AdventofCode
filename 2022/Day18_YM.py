from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

# --------------------------------------------------------------------
# DAY 18 DATA
# --------------------------------------------------------------------

data = get_data(day = 18).splitlines()
data_points = [eval(point) for point in data]

# --------------------------------------------------------------------
# SOLVE PART 1
# --------------------------------------------------------------------

def neighbors(coordinate):
    x, y, z = coordinate
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]
    
part1 = sum(neighbor not in data_points for point in data_points for neighbor in neighbors(point))

# SUBMIT PART 1
submit(part1, part='a')

# --------------------------------------------------------------------
# SOLVE PART 2
# --------------------------------------------------------------------

# CALCULATE MIN AND MAX X,Y,Z OF ALL CUBES
min_x, max_x = min(x for x, y, z in data_points), max(x for x, y, z in data_points)
min_y, max_y = min(y for x, y, z in data_points), max(y for x, y, z in data_points)
min_z, max_z = min(z for x, y, z in data_points), max(z for x, y, z in data_points)

outside = {(min_x - 1, min_y - 1, min_z - 1)}

queue = list(outside)

# FIND WHICH POINTS ARE FACING OUTSIDE NOW
while queue:
        for point in neighbors(queue.pop()):
            x, y, z = point
            if (
                min_x - 1 <= x <= max_x + 1
                and min_y - 1 <= y <= max_y + 1
                and min_z - 1 <= z <= max_z + 1
                and point not in data_points
                and point not in outside
            ):
                outside.add(point)
                queue.append(point)

part2 = sum(neighbor in outside for point in data_points for neighbor in neighbors(point))

# SUBMIT PART 2
submit(part2, part='b')