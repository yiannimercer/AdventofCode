from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit

# --------------------------------------------------------------------
# DAY 20 PUZZLE DATA
# --------------------------------------------------------------------


# RAW DATA
data = get_data(day=20).splitlines()

# CONVERT EACH COORDIANTE TO INTEGER
coordinates = [int(x) for x in data]

# --------------------------------------------------------------------
# DECRYPT FUNCTION
# --------------------------------------------------------------------


def decrypt_coordinates(coordinates_input, N):
    """DECRYPT CIRCULAR LIST OF NUMBERS BY MOVING EACH NUMBER LEFT (-) OR RIGHT (+) DEPENDING ON ITS SIGN

    E.G., INPUT = [1, 2, 3] ... DECRYPT ... OUTPUT = [2, 0, 1, 3]


    Args:
        coordinates [list]: list of coordinate values (e.g., [0, 1, 2, 3, 4, 5, -5, 4, -3, 2]) | THERE MUST BE A ZERO PRESENT
        N [int]: integer representing the amount of times we need to repeat the decryption process

    Returns:
        [list]: list of tuples that represent the original index and coordinate value pair.  List will be reordered according to decryption process
        [int]: index position of the 0 (zero)
    """
    try:
        # ENUMERATE LIST OF ENCRYPTED COORDINATES
        encrypted_coors = list(enumerate(coordinates_input))
        # CREATE SHALLOW COPY OF ABOVE SO THE ORIGINAL WON'T BE MODIFIED AND WE CAN USE THAT TO PERSERVE ORIGINAL ORDER
        new_order = encrypted_coors[:]
        # ITERATE THROUGH AND MOVE EACH VALUE
        for _ in range(N):
            for idx_value in encrypted_coors:
                i = new_order.index(idx_value)
                new_order.remove(idx_value)
                target_idx = (i + idx_value[1]) % len(new_order)
                new_order.insert(target_idx, idx_value)
            # PUT FIRST ITEM TO THE END OF THE LIST (NOT SURE WHY IT HAS IT IN THE FRONT)
            first_item = new_order[0]
            new_order = new_order[1:]
            new_order.append(first_item)

        # GET INDEX OF ZERO ELEMENT
        zero_idx = [coor for idx, coor in new_order].index(0)

        # RETURN REORDERED LIST AND ZERO INDEX
        return new_order, zero_idx
    except ValueError:
        print(
            "ENSURE THAT THE ENCRYPTED LIST OF VALUES CONTAINS A ZERO (0) AND FOLLOWS THE FORMAT IN THE DOCTSTRING"
        )
        return None


# --------------------------------------------------------------------
# SOLVE PART 1 & SUBMIT
# --------------------------------------------------------------------


part1_reorder, part1_zero_idx = decrypt_coordinates(coordinates, 1)
part1_answer = sum(
    [
        part1_reorder[(part1_zero_idx + i) % len(part1_reorder)][1]
        for i in (1000, 2000, 3000)
    ]
)
print(f"Part 1: {part1_answer}")
submit(part1_answer, part="a")

# --------------------------------------------------------------------
# SOLVE PART 2 & SUBMIT
# --------------------------------------------------------------------


# READ DATA IN AGAIN TO GET ORIGINAL ORDERING & APPLY DECRYPTION KEY - 811589153
coordinates = [int(x) for x in get_data(day=20).splitlines()]
key_coordinates = [x * 811589153 for x in coordinates]

# RUN DECRYPTION PROCESS 10 TIMES
part2_reorder, part2_zero_idx = decrypt_coordinates(key_coordinates, 10)
part2_answer = sum(
    [
        part2_reorder[(part2_zero_idx + i) % len(part2_reorder)][1]
        for i in (1000, 2000, 3000)
    ]
)
print(f"Part 2: {part2_answer}")
submit(part2_answer, part="b")
