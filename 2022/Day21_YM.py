from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit
from collections import defaultdict

# --------------------------------------------------------------------
# DAY 21 PUZZLE INPUT
# --------------------------------------------------------------------


data = get_data(day=21)

# --------------------------------------------------------------------
# MONKEY YELLER FUNCTION
# --------------------------------------------------------------------


def monkey_yeller(data_input):
    # SPLIT STRING ON NEW LINE - EACH MONKEY AND THEIR RESPECTIVE NUMBER/EQUATION IS ON ONE LINE
    monkeys_list = data_input.splitlines()
    # SPLIT EACH LINE ON THE COLON INTO A TUPLE, FIRST VALUE IS THE MONKEY NAME, SECOND IS THE VALUE THEY SCREAM
    monkeys = [tuple(monkey.split(":")) for monkey in monkeys_list]
    # DICTIONARIES TO HOLD THE THREE TYPES OF MONKEY YELLS
    all_monkeys = defaultdict()
    numbers = defaultdict()
    equations = defaultdict()
    # STORE ALL MONKEYS AND WHAT THEY ARE YELLING IN TOP LEVEL DICT
    for key, value in monkeys:
        all_monkeys[key] = value.strip().split(" ")
    # SEPERATE MONKEYS INTO TWO DICTS | (1) IF THEY HAVE A NUMBER OR (2) THEY HAVE AN EQUATION
    for key, value in all_monkeys.items():
        if len(value) == 1:
            numbers[key] = value[0]
        else:
            equations[key] = value

    # ITERATE BETWEEN EQUATIONS AND NUMBERS DICT, REPLACING EACH MONKEY NAME WITH ITS VALUE AND SOLVING EQUATIONS WHEN POSSIBLE
    while len(equations) > 1:
        for key, value in equations.items():
            for i in range(len(value)):
                if value[i] in numbers.keys():
                    value[i] = numbers[value[i]]
        # IF WE CAN SOLVE THE EQUATION, EVALUATE AND SEND TO NUMBERS DICT AND REMOVE FROM EQUATIONS DICT
        monkeys_to_remove = []
        for key, value in equations.items():
            if value[0].isdigit() and value[2].isdigit():
                value = str(eval("".join(value))).replace(".0", "")
                numbers[key] = value
                monkeys_to_remove.append(key)
        for item in monkeys_to_remove:
            equations.pop(item)

    # REPEAT PROCESS ONE MORE TIME TO SOLVE FINAL VALUE
    for key, value in equations.items():
        for i in range(len(value)):
            if value[i] in numbers.keys():
                value[i] = numbers[value[i]]
    # RETURN EQUATIONS AND NUMBER (RETURN BOTH IN CASE 'ROOT' ISN'T THE LAST MONKEY TO SOLVE)
    return equations, numbers


# --------------------------------------------------------------------
# SOLVE PART 1
# --------------------------------------------------------------------


part1_equations, part1_numbers = monkey_yeller(data)
for key, value in part1_equations.items():
    part1_answer = eval("".join(value))

# SUBMIT PART 1
submit(part1_answer, part="a")

part1_numbers["humn"]
