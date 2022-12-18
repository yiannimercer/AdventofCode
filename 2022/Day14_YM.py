from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

# --------------------------------------------------------------------
# DEFINE FUNCTIONS
# --------------------------------------------------------------------

# GET STRAIGHT LINE COORDINATES
def rock_coordinates(x1: int, y1: int, x2:int, y2:int) -> list:
    '''
    Get list of coorindates that pass through two points if on same axis:
    '''
    coordinates_list = []
    # VERTICAL STRAIGHT LINE    
    if x1 == x2:
        Xs = []
        Ys = []
        up_to_down = y2 > y1
        if up_to_down:
            y_diff = y2 - y1
        else:
            y_diff = y1 - y2
        for i in range(y_diff + 1):
            new_y = y1 + i if up_to_down else y1-i
            Ys.append(new_y)
        coordinates = list(zip([x1] * len(Ys), Ys))
    # HORIZONTAL LINE
    if y1 == y2:
        Xs = []
        Ys = []
        left_to_right = x2 > x1
        if left_to_right:
            x_diff = x2 - x1
        else:
            x_diff = x1-x2
        for i in range(x_diff + 1):
            new_x = x1 + i if left_to_right else x1-i
            Xs.append(new_x)
        coordinates = list(zip(Xs,len(Xs) * [y1]))
    for item in coordinates:
        coordinates_list.append(item)
    return coordinates_list

# GET DICTIONARY OF COORDINATES WITH ROCKS
def cave_creator(data):
    cave = {}
    for line in data:
        for i in range(len(line)):
            if isinstance(line[i], tuple):
                try:
                    x1, y1 = line[i]
                    x2, y2 = line[i+2]
                    coordinates = rock_coordinates(x1,y1,x2,y2)
                    for coor in coordinates:
                        cave[coor] = "#"
                except:
                    break
            else:
                pass
    return cave

# GET LAST Y
def largest_y(cave):
    return max(y for (_, y) in cave.keys())

# SIMULATE SAND FALL
def simulate_sand(cave):
    x = 500 
 
    for y in range(largest_y(cave)):
        # DOWN ONE STEP
        if (x, y + 1) not in cave:
            continue 
        # DOWN LEFT ONE STEP 
        elif (x - 1, y + 1) not in cave:
            x -= 1
        # DOWN RIGHT ONE cave
        elif (x + 1, y + 1) not in cave:
            x += 1
        else: 
            cave[(x, y)] = "o"
            # STOP IF WE ARE BLOCK BY STARTING POINT
            return (x, y) != (500, 0) 
    return False

# --------------------------------------------------------------------
# PART 1 SOLVE 
# --------------------------------------------------------------------

# GET INPUT INTO WORKABLE FORMAT
data = get_data(day=14, year=2022)
data = data.splitlines()
data = [line.split() for line in data]
data = [[eval(coor) if coor != "->" else "->" for coor in row] for row in data]

# GET ROCK COORDIANTES IN CAVE
cave = cave_creator(data)

# SIMUALTE SANDFALL
while simulate_sand(cave):
    pass

part_1 = sum(obj == 'o' for obj in cave.values())
print(f"{part_1} units of sand come to a rest before falling into the abyss")

# SUBMIT PART 1
submit(part_1, part='a')

# --------------------------------------------------------------------
# PART 2 SOLVE 
# --------------------------------------------------------------------

# ADD BOTTOM FLOOR 
def add_floor(cave):
    y = largest_y(cave) + 2
    for x in range(-1000, 1001):
        cave[(x, y)] = "#"
    return cave

cave = cave_creator(data)
cave_with_floor = add_floor(cave)

# SIMULATE SANDFALL
while simulate_sand(cave_with_floor):
    pass

part_2 = sum(obj == 'o' for obj in cave.values())
print(f"{part_2} units of sand come to a rest before falling into the abyss")

# SUBMIT PART 2
submit(part_2, part='b')