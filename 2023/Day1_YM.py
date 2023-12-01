from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import re
from word2number import w2n
import n2w

# --------------------------------------------------------------------
# READ IN DATA
# --------------------------------------------------------------------

data = get_data(day=1, year=2023)

# --------------------------------------------------------------------
# SOLUTION - PART 1
# --------------------------------------------------------------------

# Part 1
split_data = data.split('\n')

# List to save digits
digits_list = []

# Regular Expression to pull out all digits
for value in split_data:
    digits = re.findall('\d', value)
    digits_list.append(digits)
    
# Iterate through the digits list and sum the first and last element if len > 2

sum_list = []

for value_list in digits_list:
    if len(value_list) > 1:
        first_element = value_list[0]
        second_element = value_list[-1]
    else:
        first_element = value_list[0]
        second_element = value_list[0]
    sum_value = first_element + second_element
    sum_list.append(int(sum_value))
    
# Part 1 Answer
part1_answer = sum(sum_list)
submit(part1_answer, part='a', day=1, year=2023)

# --------------------------------------------------------------------
# SOLUTION - PART 2
# --------------------------------------------------------------------

# Found w2n & n2w package that can turn numbers to words and vice versa
print(n2w.convert(2))
print(w2n.word_to_num('five'))

letter_numbers = [n2w.convert(x) for x in range(1, 10)]
part_b_regex = re.compile(rf"(\d|{'|'.join(letter_numbers)})")
d = dict(zip(letter_numbers, "123456789"))

calibration_values = []

for line in split_data:
    nums_b = [int(d.get(x, x)) for x in part_b_regex.findall(line, overlapped=True)]
    if len(nums_b) > 1:
        first_element = str(nums_b[0])
        second_element = str(nums_b[-1])
    else:
        first_element = str(nums_b[0])
        second_element = str(nums_b[0])
    sum_element = first_element + second_element
    calibration_values.append(int(sum_element))

# Part 2 Answer
part2_answer = sum(calibration_values)
submit(part2_answer, part='b', day=1, year=2023)
