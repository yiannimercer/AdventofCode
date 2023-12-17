from aocd import get_data, submit
from dotenv import load_dotenv
import re

load_dotenv()


# --------------------------------------------------------------------
# PREPARE DATA
# --------------------------------------------------------------------

initialization_sequence_raw = get_data(day=15, year=2023).split(',')
initialization_sequence = [{key: 0} for key in initialization_sequence_raw]

example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')
example = [{key: 0} for key in example]

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


def hash_algorithm(step, current_value=0):
    """This function executes the HASH algorithm. The HASH algorithm is a way to
    turn any string of characters into a single number in the range 0 to 255.

    Args:
        step (_str_): The string that we will execute the hash algorithm against
        current_value (_int_): The current_value the string is starting at.

    Returns:
        _int_: The output of the hash algorithm for the given string 
    """
    # Convert each character of the step sring to a list of its characters
    step_list = list(step)
    # Iterate through each character
    for chr in step_list:
        # Determine the asii value of the corresponding character
        ascii_value = ord(chr)
        # Increase the current value by the ASCII code we just determined
        current_value += ascii_value
        # Set the current value to itself multiplied by 17
        current_value *= 17
        # Set the current value to the remainder of dividing itself by 256
        current_value = current_value % 256
    # Return current_value for the given string
    return str(current_value)


# Execute HASH algorithm on each item of the initialization sequence
initialization_sequence_hashed = [{k: hash_algorithm(k, v)} for d in initialization_sequence for k, v in d.items()]

# Sum values
total = sum(int(value) for d in initialization_sequence_hashed for value in d.values())

submit(total, part='a', day=15, year=2023)


# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------


def parse_step_input(initialization_sequence):
    """Parse each step in the initialization sequence into a tuple.

    Args:
        initialization_sequence (list[dict]): The initialization sequence

    Returns:
        list[tuple]: The list of parsed steps as tuples
    """
    parsed = []

    # Iterate through each dict (step) in the sequence
    for step in initialization_sequence:
        # Get the key-value pairs from the dict
        for key, value in step.items():
            original_str = key
            # Use a regex to match the pattern in the key
            match = re.match(r'([a-z]+)(.)(.*)', key)
            # Group 1 is the label letters
            label = match.group(1)
            # Group 2 is the operator
            operator = match.group(2)
            # Group 3 is focal length, empty string if no match
            focal_length = match.group(3) if match.group(3) else ""
            # Append a tuple of the parsed components
            parsed.append((label, operator, focal_length, original_str))

    # Return list of parsed step tuples
    return parsed
    
# --------------------------------------------------------------------
# Parsing Initialization Sequence
# --------------------------------------------------------------------

def parse_step_input(initialization_sequence):
    """Parse each step in the initialization sequence into a tuple."""
    parsed = []
    for step in initialization_sequence:
        match = re.match(r'([a-z]+)([-=])(\d*)', step)
        if match:
            label, operator, focal_length = match.groups()
            focal_length = int(focal_length) if focal_length else None
            parsed.append((label, operator, focal_length))
    return parsed

# --------------------------------------------------------------------
# Executing HASHMAP
# --------------------------------------------------------------------

def execute_hashmap(parsed_step, boxes):
    """Execute each step in the HASHMAP process."""
    label, operator, focal_length = parsed_step
    box_number = int(hash_algorithm(label))
    lens_in_box = next((lens for lens in boxes[box_number] if lens[0] == label), None)

    if operator == '-':
        if lens_in_box:
            boxes[box_number].remove(lens_in_box)
    elif operator == '=':
        if lens_in_box:
            lens_in_box[1] = focal_length
        else:
            boxes[box_number].append([label, focal_length])

# --------------------------------------------------------------------
# Calculating Focusing Power
# --------------------------------------------------------------------

def calculate_focusing_power(boxes):
    """Calculate the total focusing power of the lenses."""
    total_power = 0
    for box_number, lenses in enumerate(boxes):
        for slot_number, (label, focal_length) in enumerate(lenses, start=1):
            total_power += (box_number + 1) * slot_number * focal_length
    return total_power

# --------------------------------------------------------------------
# Applying the Logic to Example Data
# --------------------------------------------------------------------

# Parsing the example initialization sequence
parsed_seq = parse_step_input(initialization_sequence_raw)

# Initializing boxes for storing lenses
boxes = [[] for _ in range(256)]

# Executing HASHMAP for each step in the example
for step in parsed_seq:
    execute_hashmap(step, boxes)

# Calculating the total focusing power for the example
focusing_power = calculate_focusing_power(boxes)

submit(focusing_power, part='b', day=15, year=2023)