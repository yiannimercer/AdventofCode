from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

# --------------------------------------------------------------------
# READ DATA
# --------------------------------------------------------------------

raw_data = get_data(day=5, year=2023)
data = get_data(day=5, year=2023).splitlines()
seeds = data[0].split(': ')[1].split()
seeds = [int(seed) for seed in seeds]

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------

# Parse Data into Dictionary
mapping_dict = {}

for line in data[2:]:
    if 'map:' in line:
        # Extract the map name and initialize an empty list for its values
        current_map = line.strip()[0:-1]
        mapping_dict[current_map] = []
    elif current_map and line.strip():
        # Convert each split string to an integer and add to the map's list
        mapping_dict[current_map].append([int(num) for num in line.strip().split()])


def create_mapping_tuples(mapping_dict, seed_list):
    final_mappings = {}
    current_values = set(seed_list)

    for map_key, specific_map in mapping_dict.items():
        final_mappings[map_key] = []
        new_values = set()

        # Map each value directly if it's not in the range of any mapping
        all_mapped_ranges = [(source_start, source_start + range_length) for _, source_start, range_length in specific_map]
        unmapped_values = {value for value in current_values if not any(start <= value < end for start, end in all_mapped_ranges)}
        final_mappings[map_key].extend([(value, value) for value in unmapped_values])
        new_values.update(unmapped_values)

        # Process mappings
        for destination_start, source_start, range_length in specific_map:
            for value in current_values:
                if source_start <= value < source_start + range_length:
                    destination_value = destination_start + (value - source_start)
                    final_mappings[map_key].append((value, destination_value))
                    new_values.add(destination_value)

        current_values = new_values

    return final_mappings

final_mappings = create_mapping_tuples(mapping_dict, seeds)

location_map = final_mappings['humidity-to-location map']

locations = []

for source, destination in location_map:
    locations.append(destination)
    
min_location_num = min(locations)

submit(min_location_num, part='a', day=5, year=2023)

# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------


def create_mapping_tuples(mapping_dict, seed_ranges):
    # Convert seed ranges to pairs of (start, end)
    current_ranges = [(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]) for i in range(0, len(seed_ranges), 2)]

    for map_key, specific_map in mapping_dict.items():
        new_ranges = []

        while current_ranges:
            start, end = current_ranges.pop(0)
            for destination_start, source_start, range_length in specific_map:
                overlapping_start = max(start, source_start)
                overlapping_end = min(end, source_start + range_length)

                if overlapping_start < overlapping_end:
                    # Adjust the range based on the mapping
                    new_start = overlapping_start - source_start + destination_start
                    new_end = overlapping_end - source_start + destination_start
                    new_ranges.append((new_start, new_end))

                    # Split the range if only part of it overlaps
                    if overlapping_start > start:
                        current_ranges.append((start, overlapping_start))
                    if overlapping_end < end:
                        current_ranges.append((overlapping_end, end))
                    break
            else:
                # Keep the range unchanged if no overlap
                new_ranges.append((start, end))

        current_ranges = new_ranges

    return current_ranges

final_mappings2 = create_mapping_tuples(mapping_dict, seeds)
    
locations2 = [value for value, _ in final_mappings2]

min_location_num2 = min(locations2)

submit(min_location_num2, part='b', day=5, year=2023)