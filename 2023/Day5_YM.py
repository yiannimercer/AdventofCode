from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()

# --------------------------------------------------------------------
# READ DATA
# --------------------------------------------------------------------

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

# Convert initial seed list to include all seeds
def create_mapping_tuples(mapping_dict, seed_list):
    final_mappings = {}
    current_values = set()
    
    # Generate the initial set of values from the seed ranges
    for i in range(0, len(seed_list), 2):
        start, length = seed_list[i], seed_list[i + 1]
        current_values.update(range(start, start + length))

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

final_mappings2 = create_mapping_tuples(mapping_dict, seeds)