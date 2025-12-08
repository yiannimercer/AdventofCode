# %% 
from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit

# %% 

data = get_data(day=6, year=2025).splitlines()

# Process data
for i in range(len(data)):
    if i == 4:
        data[i] = [x for x in data[i].split(' ') if x != '']     
    else:
        data[i] = [int(x) for x in data[i].split(' ') if x != ''] 


# %%

# ------------------------------------------------
# PUZZLE 1 
# ------------------------------------------------

columns = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        if isinstance(data[i][j], int):
            if j not in columns:
                columns[j] = {'digits': [None], 'op': None}
            columns[j]['digits'].append(data[i][j])
        else:
            columns[j]['op'] = data[i][j]
    
# Iterate through each column and perform the operation on the digits
answer_a = 0
for col in columns.values():
    digits = [d for d in col['digits'] if d is not None]
    if col['op'] == '+':
        answer_a += sum(digits)
    elif col['op'] == '*':
        prod = 1
        for d in digits:
            prod *= d
        answer_a += prod
    
# %%

submit(answer_a, part="a", day=6, year=2025)
# %%

# ------------------------------------------------
# PUZZLE 2 - TREATING INPUT AS GRID
# ------------------------------------------------


from utils.grid import Grid

# Load data
data = get_data(day=6, year=2025).splitlines()

sample = [
    '123 328  51 64 ',
    ' 45 64  387 23 ',
    '  6 98  215 314',
    '*   +   *   +  '
]

# Initiate grid
grid = Grid(data)

blocks = {}
block_num = 0

# Process each section of the grid
for col_numb in range(grid.width):
    col_values = grid.col_values(col_numb)
    if "*" in col_values or "+" in col_values:
        # Initialize the block variables
        current_operation = "*" if "*" in col_values else "+"
        current_block = []
        blocks[block_num] = {
            'operation': current_operation,
            'values': current_block
        }
        # Process value and append to list 
        value = int(col_values.replace("*", "").replace("+", "").strip())
        current_block.append(value)

    elif col_values.strip() == '':
        block_num += 1
        continue
        
    else:
        # Process value and append to list 
        value = col_values.strip()
        value = int(value)
        current_block.append(value)

# Iterate through the blocks and sum or multiply the values based on the operation
answer_b = 0
for block in blocks.values():
    if block['operation'] == '+':
        total_sum = sum(block['values'])
        answer_b += total_sum
    elif block['operation'] == '*':
        total_prod = 1
        for num in block['values']:
            total_prod *= num
        answer_b += total_prod
        
# %% 

submit(answer_b, part="b", day=6, year=2025)
        
        
        
        
    
    
        


# %%
