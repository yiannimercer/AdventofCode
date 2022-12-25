from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit


# --------------------------------------------------------------------
# DAY 25 PUZZLE INPUT
# --------------------------------------------------------------------


data = get_data(day=25)

# --------------------------------------------------------------------
# SNAFU TO DECIMAL CONVERTER
# --------------------------------------------------------------------

snafu = "1=-0-2"

snafu_split = [*snafu]

snafu_decimal_places = [1, 5]

while len(snafu_decimal_places) < 25:
    last_item = snafu_decimal_places[-1]
    new_item = last_item * 5
    snafu_decimal_places.append(new_item)

decimals_needed = len(snafu_split)

snafu_decimals_needed = snafu_decimal_places[:6][::-1]

equations = []

for i in range(len(snafu_split)):
    value = snafu_split[i]
    if value == "-":
        value = "-1"
    elif value == "=":
        value = "-2"
    equations.append(str(value) + "*" + str(snafu_decimals_needed[i]))

sum([eval(item) for item in equations])


def snafu_to_decimal(snafu_string):
    # SPLIT SNAFU STRING WITH EACH CHRACTER BEING AN ITEM IN A LIST
    snafu_split = [*snafu_string]
    # GENERATE LIST OF SNAFU DECIMAL PLACES, INCREMENTING BY A PRODUCT 5
    snafu_decimal_places = [1, 5]
    while len(snafu_decimal_places) < 25:
        last_item = snafu_decimal_places[-1]
        new_item = last_item * 5
        snafu_decimal_places.append(new_item)
    # GRAB THE NUMBER OF DECIMALS PLACES WE'LL NEED FOR THIS CONVERSION AND REVERSE THE LIST
    decimals_needed = len(snafu_split)
    snafu_decimals_needed = snafu_decimal_places[:decimals_needed][::-1]
    # ITERATE THROUGH AND MULTIPLE EACH VALUE BY IT'S CORRESPONDING DECIMAL PLACE
    equations = []
    for i in range(len(snafu_split)):
        value = snafu_split[i]
        if value == "-":
            value = "-1"
        elif value == "=":
            value = "-2"
        equations.append(str(value) + "*" + str(snafu_decimals_needed[i]))
    # RETURN THE SUM OF THE EVALUATED EQUATIONS
    return sum([eval(item) for item in equations])


def decimal_to_snafu(decimal):

    snafu = ""

    i = 0
    while True:
        if ((5**i) * 2) >= decimal:
            break
        i += 1

    while i >= 0:
        options = {
            "=": decimal + (5**i) * 2,
            "-": decimal + (5**i),
            "0": decimal,
            "1": decimal - (5**i),
            "2": decimal - (5**i) * 2,
        }
        option = "="
        lowest = options[option]
        for s in ("-", "0", "1", "2"):
            if abs(options[s]) < lowest:
                option = s
                lowest = abs(options[s])
        decimal = options[option]
        snafu += option
        i -= 1

    return snafu


# --------------------------------------------------------------------
# SOLVE PART 1
# --------------------------------------------------------------------

decimals = []
for snafu in data.splitlines():
    decimal = snafu_to_decimal(snafu)
    decimals.append(decimal)
part1 = decimal_to_snafu(sum(decimals))
submit(part1, part="a")
