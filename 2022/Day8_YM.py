from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()
from collections import defaultdict



# PART A 

def is_visible(forest, height, width):
    
    # GLOBAL STORAGE CONTAINERS
    tree_visibility = defaultdict(list)    
    visible_bottom_count = []
    visible_top_count = []
    visible_left_count = []
    visible_right_count = []
    all_visible_trees = []
    
    for x in range(1, height-1): 
        for y in range(1, width-1):     
                   
            # BOTTOM CHECK
            visible_bottom = all([int(forest[i][y][0]) < int(forest[x][y][0]) for i in range(x+1, height)])
            visible_bottom_count.append(visible_bottom)
            tree_visibility[forest[x][y]].append(visible_bottom)                        
            
            # TOP CHECK
            visible_top = all(int(forest[x][y][0]) > int(forest[i][y][0]) for i in range(x-1, -1, -1)) 
            visible_top_count.append(visible_top)
            tree_visibility[forest[x][y]].append(visible_top)

            # LEFT CHECK
            visible_left = all(int(forest[x][i][0]) < int(forest[x][y][0]) for i in range(y-1, -1, -1)) # REMEMBER TO REMOVE THE FINAL INDEX [0] ON THE REAL DATASET
            visible_left_count.append(visible_left)
            tree_visibility[forest[x][y]].append(visible_left)
            
            # RIGHT CHECK
            visible_right = all(int(forest[x][i][0]) < int(forest[x][y][0]) for i in range(y+1, width)) # REMEMBER TO REMOVE THE FINAL INDEX [0] ON THE REAL DATASET
            visible_right_count.append(visible_right)
            tree_visibility[forest[x][y]].append(visible_right)
    
    # TOTAL NUMBER OF INTERIOR TREES WITH AT LEAST ONE DIRECTION OF VISIBILITY
    for tree in tree_visibility.keys():
        if any(tree_visibility[tree]):
            all_visible_trees.append(tree)
           
    # RETURN COUNT
    return len(all_visible_trees)
        
def scenic_score(forest, x, y, height, width):

    # BOTTOM
    for i in range(x+1, height):
        if int(forest[i][y]) >= int(forest[x][y]):
            distance_bottom = i - x
            break
    else:
        distance_bottom = height - x - 1
            
    # TOP
    for i in range(x-1, -1, -1):
        if int(forest[i][y]) >= int(forest[x][y]):
            distance_top = x - i
            break
    else:
        distance_top = x
        
    # LEFT
    for i in range(y-1, -1, -1):
        if int(forest[x][i]) >= int(forest[x][y]):
            distance_left = y - i
            break
    else:
        distance_left = y
                    
    # RIGHT
    for i in range(y+1, width):
        if int(forest[x][i]) >= int(forest[x][y]):
            distance_right = i - y
            break
    else:
        distance_right = width - y - 1
                
    # GET SCENIC SCORE
    scenic_score = distance_left * distance_right * distance_top * distance_bottom

    # RETURN SCENIC SCORE
    return scenic_score
            
# GET AOCD DATA
data = get_data(day=8, year=2022)

# SPLIT LINES AND MAKE EACH TREE IT'S OWN LIST ITEM
forest = data.splitlines()

forest = [[str(tree) for tree in line] for line in forest]

height = len(forest)
width = len(forest[0])

for i in range(len(forest)):
    for j in range(len(forest[i])):
        forest[i][j] = forest[i][j] + f"_{i}_{j}"

# PART A
total = 2*(height + width) - 4
total_a  = is_visible(forest, height, width)
total_a += total
print(f"Visible Tree Count: {total_a}")

# PART B
forest = data.splitlines()

forest = [[int(tree) for tree in line] for line in forest]

height = len(forest)
width = len(forest[0])
sscores = []
for x in range(1, height): 
    for y in range(1, width):
        sscore = scenic_score(forest, x, y, height, width)
        sscores.append(sscore)
part_b = max(sscores)


submit(part_b, day=8, year=2022)
