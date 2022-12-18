from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import math
from parse import parse

# --------------------------------------------------------------------
# GET TODAYS DATA
# --------------------------------------------------------------------

data = get_data(day=15).splitlines()

# --------------------------------------------------------------------
# PUZZLE FUNCTIONS
# --------------------------------------------------------------------

def manhattan(x, y):
        #x[0], y[0], x[1], y[1] = int(x[0]), int(y[0]), int(x[1]), int(y[1])
        return abs(x[0] - y[0]) + abs(x[1] - y[1])
    
def parse_notes(note):
    template = "Sensor at x={sensorX}, y={sensorY}: closest beacon is at x={beaconX}, y={beaconY}"
    notes_parsed = parse(template, note).named
    note
    return notes_parsed    

def get_report_distance(input):
    reports = []
    for line in input:
        report = {}
        locations = parse_notes(line)
        report['sensor'] = (int(locations['sensorX']), int(locations['sensorY']))
        report['beacon'] = (int(locations['beaconX']), int(locations['beaconY']))
        report['distance'] = manhattan(report['beacon'], report['sensor'])
        reports.append(report)
    return reports



def find_blocked_bounds(reports, row):
    left_bound = None
    right_bound = None
    for report in reports:
        (sensor_x, sensor_y) = report['sensor']
        cols_in_row = report['distance'] - abs(row - sensor_y)
        if cols_in_row >= 0:
            if left_bound is None:
                left_bound = sensor_x - cols_in_row
            else:
                left_bound = min(left_bound, sensor_x - cols_in_row)
            if right_bound is None:
                right_bound = sensor_x + cols_in_row
            else:
                right_bound = max(right_bound, sensor_x + cols_in_row)
    return left_bound, right_bound
        
def solve_1(data, row):
    reports = get_report_distance(data)
    (left_bound, right_bound) = find_blocked_bounds(reports, row)
    return right_bound - left_bound

# --------------------------------------------------------------------
# SOLVE PART 1
# --------------------------------------------------------------------
    
part_1 = solve_1(data, 2000000)
submit(part_1, part='a', day=15)

# --------------------------------------------------------------------
# PART 2 FUNCTION
# --------------------------------------------------------------------

def find_beacon(distances, row, max_val):
    min_left_bound = None
    max_left_bound = None
    ranges = []
    for distance in distances:
        (sensor_x, sensor_y) = distance['sensor']
        cols_in_row = distance['distance'] - abs(row - sensor_y)
        if cols_in_row >= 0:
            left_bound = max(0, sensor_x - cols_in_row)
            right_bound = min(sensor_x + cols_in_row, max_val)
            ranges.append((left_bound, right_bound))
    sorted_ranges = sorted(ranges)
    curr_min_x = sorted_ranges[0][0]
    curr_max_x = sorted_ranges[0][1]
    for curr_range in sorted_ranges[1:]:
        (lx, rx) = curr_range
        if curr_min_x <= rx and lx <= curr_max_x: # overlap
            curr_min_x = min(curr_min_x, lx)
            curr_max_x = max(curr_max_x, rx)
        else:
            return (lx - curr_max_x) - 1 + curr_max_x
        
def solve_2(data, max_val, freq_mult):
    distances = get_report_distance(data)
    for row in range(max_val + 1):
        beacon = find_beacon(distances, row, max_val)
        if beacon:
            break
    freq = beacon * freq_mult + row
    return freq

# --------------------------------------------------------------------
# SOLVE PART 2
# --------------------------------------------------------------------

part_2 = solve_2(data,  4000000, 4000000)
submit(part_2, part='b',day=15)