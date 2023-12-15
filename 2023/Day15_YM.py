from aocd import get_data, submit
from dotenv import load_dotenv
import re

load_dotenv()


# --------------------------------------------------------------------
# PREPARE DATA
# --------------------------------------------------------------------

initialization_sequence = get_data(day=15, year=2023).split(',')
initialization_sequence = [{key: 0} for key in initialization_sequence]

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


def hash_algorithm(step, current_value):
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


def execute_hashmap(parsed_step, boxes, initialization_sequence_hashed):
    """_summary_

    Args:
        parsed_step (_tuple_): _description_
        boxes (_list_): _description_
        initialization_sequence_hashed (_list_): 
    """
    # Extract label and operator from the parsed_step
    original_str = parsed_step[3]
    label, operator = parsed_step[0], parsed_step[1]
    # Grab box number from the hashed initialization sequence
    box_number = next((d[original_str] for d in initialization_sequence_hashed if original_str in d), None)
    
    if operator == '-':
        # Remove dictionaries containing the label from the box with box_number
        for box in boxes:
            if box_number in box:
                box[box_number] = [d for d in box[box_number] if label not in d]
                break
    elif operator == "=":
        # Update the value of the label key in the box with box_number, if present; otherwise, append a new dictionary
        focal_length = parsed_step[2]
        label_found = False

        for box in boxes:
            if box_number in box:
                for d in box[box_number]:
                    if label in d:
                        d[label] = focal_length
                        label_found = True
                        break

                if not label_found:
                    box[box_number].append({label: focal_length})

                break
    return boxes


def calculate_focusing_power():
    
    
# Iterate through and run HASHMAP

# Create a list of empty boxes, 0 - 255
boxes = [{str(box_num): []} for box_num in list(range(256))]

parsed_initialization_seq = parse_step_input(initialization_sequence_hashed)


for step in parsed_initialization_seq:
    boxes = execute_hashmap(step, boxes, initialization_sequence_hashed)
    
