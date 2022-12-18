from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import re
import numpy as np

data = get_data(day=10)

program = data.splitlines()

sample = open("sample_input.txt").read()
sample_program = sample.splitlines()

def singal_strength(program):
    # INITIATE START OF CYCLES
    cycles = {1:1}
    # FIRST CYCLE
    cycle = 1 
    for line in program:
        # IF ADDX-V LINE, PERFORM TWO CYCLES, FIRST CYCLE, X REMAINS THE SAME, SECOND CYCLE, X = LAST X + V
        if "add" in line:
            # FIND DIGITS (POSITIVE & NEGATIVE IN LINE USING REGEX)
            V = int(re.findall(r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', line)[0])
            # PERFORM TWO CYCLES
            for i in range(1, 3):
                # GRAB THE X FROM THE MOST RECENT CYCLE PERFORMED
                X_before  = list(cycles.items())[-1][1]
                # INCREASE CYCLE BY ONE
                cycle += 1 
                # SET THIS NEW CYCLE TO THE SAME X AS THE MOST RECENT ONE
                cycles[cycle] = X_before
                # ON SECOND CYCLE ADD THE OLD X TO THE NEW X
                if i == 2:
                    cycles[cycle] = X_before + V
        # IF IT'S A NEW NOOP LINE, RUN THE NEXT CYCLE, BUT USE MOST RECENT X 
        else:
            X_before  = list(cycles.items())[-1][1]
            cycle += 1
            cycles[cycle] = X_before
    # INITITATE LIST OF CYCLES WE'RE INTERESTED IN
    cycles_of_interest = [20, 60, 100, 140, 180, 220]
    # INITIATE EMPTY LIST TO HOLD PRODUCTS
    X_values = []
    # GRAB CYCLE VALUE FOR EACH CYCLE OF INTEREST AND MULTIPLY BY ITS CYCLE NUMBER
    for cycle in cycles_of_interest:
        # APPEND PRODUCTS TO LIST
        X_values.append(cycles[cycle] * cycle)
    # CALCULATE AND RETURN SUM OF THESE SIGNALS
    sum_of_signal_strength = sum(X_values)
    return cycles, sum_of_signal_strength

# PART A
cycles, part_a = singal_strength(program)
submit(part_a, part='a')

# PART B
x, signal = 1, 0
CRT = ""
# ITERATE THROUGH DATA AND SPLIT EACH LINE INTO TWO (ONE LINE IS THE ADDX, THE SECOND LIST IS V)
# IF NOOP LINE, ONE LINE
# EACH LINE REPRESENTS A CYCLE
for cycle_num, step in enumerate(data.split(), start=1):
    signal += cycle_num * x if cycle_num % 40 == 20 else 0
    CRT += "#" if (cycle_num - 1) % 40 - x in (-1, 0 ,1) else " "
    if step[-1].isdigit():
        x += int(step)
for i in range(0, len(CRT), 40):
    print(CRT[i : i + 40])

part_b = 'ZGCJZJFL'
submit(part_b, part='b')