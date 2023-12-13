from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------
# READ DATA
# --------------------------------------------------------------------

condition_records = get_data(day=12, year=2023).splitlines()

condition_records = [row.split(' ') for row in condition_records]

condition_records_formatted = []
for row in condition_records:
    springs = list(row[0])
    damage_size = list(int(x) for x in row[1].split(','))
    condition_records_formatted.append((springs, damage_size))
    
    
# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------

condition_records_formatted[0]

def valid_arrangement(spring_line):
    