from aocd import get_data, submit
from dotenv import load_dotenv
load_dotenv()
from math import prod
from parse import parse
import re
from dataclasses import dataclass
import math

data = get_data(day=11)

sample = open('sample_input.txt').read()
sample_notes = sample.split('\n\n')

def parse_notes(note):
    template = '''Monkey {monkey_number}:
  Starting items: {items}
  Operation: new = {x} {operation} {y}
  Test: divisible by {test:d}
    If true: throw to monkey {true:d}
    If false: throw to monkey {false:d}'''
    notes_parsed = parse(template, note).named
    notes_parsed["items"] = notes_parsed["items"].split(", ")
    notes_parsed['count'] = 0 
    return notes_parsed

def apply_operation(x:int, y:int, operation:str):
    """Apply operation to a and b"""
    if x == "old":
        y = x
    else:
        y = int(y)
    
    match operation:
        case "+":
            return x + y
        case "*":
            return x * y
        case "-":
            return x - y
        case "/":
            return x / y
        case other:
            raise Exception(f'Unknown operation {other}')

# PART 1
notes = data.split('\n\n')
monkeys = [parse_notes(note) for note in notes]

for round in range(20):
    # Monkeys
    for monkey in monkeys:
        # Items
        for _ in range(len(monkey['items'])):
            monkey['count'] += 1

            # apply operation
            monkey['items'][0] = int(monkey['items'][0])
            x = int(monkey['x']) if monkey['x'].isdigit() else int(monkey['items'][0])
            y = int(monkey['y']) if monkey['y'].isdigit() else int(monkey['items'][0])
            monkey['items'][0] = apply_operation(x, y, monkey['operation'])
            
            # monkey gets bored
            monkey['items'][0] //= 3
            monkey['items'][0] = int(monkey['items'][0])

            # test
            if not monkey['items'][0] % monkey['test']:
                monkeys[monkey['true']]['items'].append(monkey['items'][0])
            else:
                monkeys[monkey['false']]['items'].append(monkey['items'][0])
            monkey['items'].remove(monkey['items'][0])
                
    print(f'Round {round+1}')
    for i, monkey in enumerate(monkeys):
        print(f'Monkey {i} : {monkey["items"]} ({monkey["count"]})')
    print(f'Part 1 : {prod(sorted([monkey["count"] for monkey in monkeys])[-2:])}')
    part1 = prod(sorted([monkey["count"] for monkey in monkeys])[-2:])

submit(part1, day=11, part='a')

# PART 2 - COULD NOT FIGURE IT OUT | HAD TO LEAD ON https://github.com/Kokopak/advent2022/blob/master/day11/day11.py FOR HELP
import operator
import re
from copy import deepcopy

MAP_SIGN = {
    "+": operator.add,
    "*": operator.mul,
    "/": operator.truediv,
    "-": operator.sub,
}


def parse_monkey(s):
    regex = (
        r"Monkey (\d+):\n"
        r"  Starting items:([ \d+,]*)\n"
        r"  Operation: new = old (.) (.+)\n"
        r"  Test: divisible by (\d+)\n"
        r"    If true: throw to monkey (\d+)\n"
        r"    If false: throw to monkey (\d+)"
    )
    (
        monkey,
        items,
        operator,
        operator_value,
        divisible_by,
        true_monkey,
        false_monkey,
    ) = re.findall(regex, s)[0]

    return monkey, {
        "items": list(map(int, items.split(","))),
        "operator": MAP_SIGN[operator],
        "operator_value": operator_value,
        "divisible_by": divisible_by,
        "if_true": true_monkey,
        "if_false": false_monkey,
        "inspected_items": 0,
    }


def get_monkey_business(n, monkeys, small_number=False):
    total_modulo = 1
    for modulo in [int(monkeys[monkey]["divisible_by"]) for monkey in monkeys]:
        total_modulo *= modulo

    for _ in range(n):
        for monkey in monkeys:
            for i in range(len(monkeys[monkey]["items"])):
                item = monkeys[monkey]["items"].pop(0)

                operator_value = monkeys[monkey]["operator_value"]
                operator_value = (
                    int(operator_value) if operator_value != "old" else item
                )

                divisible_by = int(monkeys[monkey]["divisible_by"])

                worry_level = monkeys[monkey]["operator"](item, operator_value)
                worry_level //= 3 if small_number else 1

                monkeys[monkey]["inspected_items"] += 1

                if worry_level % divisible_by == 0:
                    monkeys[monkeys[monkey]["if_true"]]["items"].append(
                        worry_level % total_modulo
                    )
                else:
                    monkeys[monkeys[monkey]["if_false"]]["items"].append(
                        worry_level % total_modulo
                    )

    inspected_items = [monkeys[monkey]["inspected_items"] for monkey in monkeys]

    return operator.mul(*sorted(inspected_items, reverse=True)[:2])


monkeys = {}
with open("day11_input.txt") as f:
    s = ""
    for l in f.readlines():
        if l == "\n":
            monkey, monkey_def = parse_monkey(s)
            monkeys[monkey] = monkey_def
            s = ""
        else:
            s += l

    monkey, monkey_def = parse_monkey(s)
    monkeys[monkey] = monkey_def

p1 = get_monkey_business(20, deepcopy(monkeys), small_number=True)
print(p1)
p2 = get_monkey_business(10000, deepcopy(monkeys))
print(p2)
submit(p2, day=11)