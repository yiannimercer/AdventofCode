from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

import numpy as np

#------------------------------------------------
# READ DATA IN
#------------------------------------------------


data = get_data(day=6, year=2023).splitlines()

winning_records = {'race1': 0,
                   'race2': 0,
                   'race3': 0,
                   'race4': 0}

times = data[0].split()[1:]
distance_records = data[1].split()[1:]

times = [int(x) for x in times]
distance_records = [int(x) for x in distance_records]

race_info = list(zip(times,distance_records))

for key, (time, record) in zip(winning_records, race_info):
    winning_records[key] = [(time, record), 0]

for race_num in winning_records:
    race = winning_records[race_num]
    race_time = race[0][0]
    distance_record = race[0][1]
    #times_record_beat = race[1]
    for i in range(race_time):
        time_to_race = race_time - i
        speed = i
        distance_moved = time_to_race * speed
        if distance_moved > distance_record:
            race[1] += 1

times_record_broke = []

for race in winning_records:
    times_record_broke.append(winning_records[race][1])
    
part1_answer = np.prod(times_record_broke)
            
submit(part1_answer, part='a', day=6, year=2023)

#------------------------------------------------
# PART 2 
#------------------------------------------------

times = data[0].split()[1:]
distance_records = data[1].split()[1:]

single_race_time = int(''.join(times))
single_distance_record = int(''.join(distance_records))

part2_answer = 0

for i in range(single_race_time):
        time_to_race = single_race_time - i
        speed = i
        distance_moved = time_to_race * speed
        if distance_moved > distance_record:
            part2_answer += 1


submit(part2_answer, part='b', day=6, year=2023)      
         
        