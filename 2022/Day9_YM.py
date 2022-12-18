from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

data = get_data(day=9)

motions = data.splitlines()

def move_tails(heads: dict, tails: dict) -> dict:
    # If heads and tails are at the same position, we don't move the tails
    if heads == tails:
        return tails
    
    # If tails touches the heads (directly or diagonaly), we don't move the tails
    if abs(heads['x'] - tails['x']) <= 1 and abs(heads['y'] - tails['y']) <= 1:
        return tails
    
    # If heads and tails are on the same axis, we move the tails on the same axis
    if tails['x'] == heads['x']:
        if tails['y'] > heads['y']:
            tails['y'] -= 1
        else:
            tails['y'] += 1
        return tails
    elif tails['y'] == heads['y']:
        if tails['x'] > heads['x']:
            tails['x'] -= 1
        else:
            tails['x'] += 1
        return tails
    
    # If heads and tails are on different axis, we move the tails diagonaly
    if tails['x'] > heads['x'] and tails['y'] > heads['y']:
        tails['x'] -= 1
        tails['y'] -= 1
    elif tails['x'] > heads['x'] and tails['y'] < heads['y']:
        tails['x'] -= 1
        tails['y'] += 1
    elif tails['x'] < heads['x'] and tails['y'] > heads['y']:
        tails['x'] += 1
        tails['y'] -= 1
    elif tails['x'] < heads['x'] and tails['y'] < heads['y']:
        tails['x'] += 1
        tails['y'] += 1
    return tails

visited = [] # [] of (x, y) of visited points by the tails
tails = {'x': 0, 'y': 0}
heads = {'x': 0, 'y': 0}

for motion in motions:
    direction = motion[0]
    distance = int(motion[2:])
    for i in range(distance):
        if direction == 'U':
            heads['y'] += 1
        elif direction == 'D':
            heads['y'] -= 1
        elif direction == 'L':
            heads['x'] -= 1
        elif direction == 'R':
            heads['x'] +=1
        
        move_tails(heads, tails)
        if (tails['x'], tails['y']) not in visited:
            visited.append((tails['x'], tails['y']))

# PART 1
print(f'Part 1 : {len(visited)}')
part_1 = len(visited)
submit(part_1, day=9, year=2022)

# PART 2 - DELAY TAILS BY 9 SPACES

# HAD TO REMAKE ABOVE FUNCTION TO ACCOUNT FOR TRAILING TAILS LENGTH (PART A = TRAILING 2, PART B = TRAILING 9)
def simulate_motion(motions, length):
    position = [[0, 0] for _ in range(length)]
    visited = set()
    for motion in motions:
        direction, value = motion.split()
        for _ in range(int(value)):
            visited.add(tuple(position[-1]))
            if direction == "D":
                position[0][1] += 1
            elif direction == "U":
                position[0][0] += 1
            elif direction == "L":
                position[0][0] -= 1
            elif direction == "R":
                position[0][1] += 1
            for i, ((headsX, headsY), (tailsX, tailsY)) in enumerate(zip(position, position[1:])):
                if abs(headsX - tailsX) > 1:
                    tailsX += 1 if headsX > tailsX else -1
                    if abs(headsY - tailsY) > 0:
                            tailsY += 1 if headsY > tailsY else -1
                elif abs(headsY - tailsY) > 1:
                    tailsY += 1 if headsY > tailsY else -1
                    if abs(headsX - tailsX) > 0:
                        tailsX += 1 if headsX > tailsX else -1
                position[i + 1][0] = tailsX
                position[i + 1][1] = tailsY

    visited.add(tuple(position[-1]))
    
    return len(visited)
    
simulate_motion(motions, 2)    

def simulate_movement(motions, length):
    position = [[0, 0] for _ in range(length)]
    visited = set()
    for motion in motions:
        direction, value = motion.split()
        for _ in range(int(value)):
            visited.add(tuple(position[-1]))
            if direction == "D":
                position[0][1] += 1
            elif direction == "U":
                position[0][1] -= 1
            elif direction == "L":
                position[0][0] -= 1
            elif direction == "R":
                position[0][0] += 1
            for i, ((headsX, headsY), (tailsX, tailsY)) in enumerate(zip(position, position[1:])):
                if abs(headsX - tailsX) > 1:
                    tailsX += 1 if headsX > tailsX else -1
                    if abs(headsY - tailsY) > 0:
                        tailsY += 1 if headsY > tailsY else -1
                elif abs(headsY - tailsY) > 1:
                    tailsY += 1 if headsY > tailsY else -1
                    if abs(headsX - tailsX) > 0:
                        tailsX += 1 if headsX > tailsX else -1
                position[i + 1][0] = tailsX
                position[i + 1][1] = tailsY

    visited.add(tuple(position[-1]))

    return len(visited)

# MAKE SURE WE GET SAME ANSWER AS ABOVE FOR PART 1
simulate_movement(motions, 2)

# PART 2
part_2 = simulate_movement(motions, 10)
print(f"Part 2 Answer: {part_2}")
submit(part_2, day =9)
                    
