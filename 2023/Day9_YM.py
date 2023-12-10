from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

#------------------------------------------------
# READ DATA IN
#------------------------------------------------

data = get_data(day=9, year=2023).splitlines()

#------------------------------------------------
# PREPARE DATA 
#------------------------------------------------

oasis_report = [reading.split() for reading in data]
oasis_report = [[int(item) for item in sublist] for sublist in oasis_report]

#------------------------------------------------
# PART 1
#------------------------------------------------


def calcualte_differences(report_line):
    diff_data = []
    diff_data.append(report_line)
    while any(report_line):
        # Calculate the differences for the current data
        report_line = [t[1] - t[0] for t in zip(report_line, report_line[1:])]
        diff_data.append(report_line)
    return diff_data

def extrapolate_line(difference_line):
    difference_line[-1].append(0)
    # Iterate in reverse to add values
    for i in range(len(difference_line) - 2, -1, -1):
            # Calculate the sum of the last element of the current list and the last element of the next list
            new_value = difference_line[i][-1] + difference_line[i+1][-1]
            difference_line[i].append(new_value)
    return difference_line[0][-1]

extrapolated_values = []
for report_line in oasis_report:
    report_line_diffs = calcualte_differences(report_line)
    extrapolated_value = extrapolate_line(report_line_diffs)
    extrapolated_values.append(extrapolated_value)
    
part1_answer = sum(extrapolated_values)

submit(part1_answer, part='a', day=9, year=2023)

#------------------------------------------------
# PART 2 
#------------------------------------------------

def extrapolate_line_backwards(difference_lines):
    # Insert a zero at the beginning of the last line
    difference_lines[-1].insert(0, 0)

    # Iterate in reverse, starting from the second-to-last line
    for i in range(len(difference_lines) - 2, -1, -1):
        # Calculate the new value as the difference between the first elements of the next and current lines
        new_value = difference_lines[i][0] - difference_lines[i+1][0]
        # Insert the new value at the beginning of the current line
        difference_lines[i].insert(0, new_value)

    return difference_lines[0][0]

backwards_extrapolated_values = []
for report_line in oasis_report:
    report_line_diffs = calcualte_differences(report_line)
    backwards_extrapolated_value = extrapolate_line_backwards(report_line_diffs)
    backwards_extrapolated_values.append(backwards_extrapolated_value) 
    
part2_answer = sum(backwards_extrapolated_values) 

submit(part2_answer, part='b', day=9, year=2023)
