from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit 
from functools import cmp_to_key

data = get_data(day=13, year=2022)

data_input = data.splitlines()

def compare(left, right):
    # INITIAL PRINT STATEMENTS WERE USED FOR DEBUGGING
    
    # IF BOTH LEFT AND RIGHT ARE INTEGERS --> RETURN 1 IF IN RIGHT ORDER, 0 IF EQUAL, -1 IS WRONG ORDER
    if isinstance(left, int):
        if isinstance(right, int):
            #print("BOTH INTEGERS")
            #print(f"COMAPRING {left} to {right}")
            return (left > right) - (left < right)
        #print("RIGHT IS NOT AN INTEGER")
        return compare([left], right)
    if isinstance(right, int):
        #print("LEFT IS NOT AN INTEGER")
        return compare(left, [right])
    # IF WE HAVE LISTS, TAKE THE FIRST ITEM OF THE LIST
    for left2, right2 in zip(left, right):
        #print("BOTH ARE LISTS")
        if r := compare(left2, right2):
            return r
    # WHICHEVER LIST RUNS OUT OF ITEMS FIRST TO COMPARE SHOULD BE SMALLER
    #print(f"COMPARING LENGTHS | LEFT LENGTH = {len(left)} vs. RIGHT LENGTH = {len(right)}")
    return compare(len(left), len(right))


# PART 1
# SEPERATE INPUT INTO COMPARISONS (LEFT & RIGHT) AND COMPARE EACH ONE, IN ORDER
part_1, part_2 = 0, 1
for i, pairs in enumerate(data.split("\n\n")):
    left, right = map(eval, pairs.splitlines())
    if compare(left, right) == -1:
        part_1 += i + 1
submit(part_1, part='a')
        
# PART 2
pairs = [eval(p) for p in data.splitlines() if p]
pairs.append([[2]])
pairs.append([[6]])
# USING CMP_TO_KEY FROM FUNCTOOLS TO SORT BASED ON FUNCTION OUTPUT
pairs.sort(key=cmp_to_key(compare))

# ITERATE THROUGH PAIRS 
for i, pair in enumerate(pairs):
    if pair == [[2]]:
        part_2 *= i + 1
    if pair == [[6]]:
        part_2 *= i + 1
submit(part_2, part='b')

