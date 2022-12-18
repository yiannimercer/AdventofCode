from dotenv import load_dotenv
load_dotenv()
from aocd import get_data, submit
import collections
import pathlib
import itertools
import parse
import sys

# --------------------------------------------------------------------
# DAY 16 PUZZLE INPUT
# --------------------------------------------------------------------

data = get_data(day=16)

# --------------------------------------------------------------------
# PART 1 FUNCTIONS
# --------------------------------------------------------------------

PATTERNS = [
    parse.compile(
        "Valve {valve} has flow rate={rate:d}; tunnel leads to valve {valves}"
    ),
    parse.compile(
        "Valve {valve} has flow rate={rate:d}; tunnels lead to valves {valves}"
    ),
]

def parse_data(puzzle_input):
    data = clean_up_valves(dict(parse_data_line(line) for line in puzzle_input.split("\n")))
    return (
        {valve: tunnels for valve, (_, tunnels) in data.items()},
        {valve: flow_rate for valve, (flow_rate, _) in data.items()},
    )

def parse_data_line(line):
    if not any((match := pattern.parse(line)) for pattern in PATTERNS):
        raise ValueError(f"bad input: {line}")
    return match["valve"], (match["rate"], match["valves"].split(", "))

def clean_up_valves(valves):
    operational = [valve for valve, (rate, _) in valves.items() if rate > 0]
    paths = {
        node: bfs({valve: tunnels for valve, (_, tunnels) in valves.items()}, node)
        for node in valves
    }
    return {
        valve: (
            rate,
            {tunnel: paths[valve][tunnel] for tunnel in operational if tunnel != valve},
        )
        for valve, (rate, _) in valves.items()
        if rate != 0 or valve == "AA"
    }
    
def bfs(graph, start):
    queue = collections.deque([(0, start)])
    paths = {}
    while queue:
        distance, node = queue.popleft()
        if node in paths:
            continue
        paths[node] = distance
        for neighbor in graph[node]:
            queue.append((distance + 1, neighbor))
    return paths

def best_flow(graph, flows, minutes):
    max_flow = 0

    queue = collections.deque([(0, 0, "AA", set(graph) - {"AA"})])
    while queue:
        minute, flow, current, closed = queue.popleft()
        steps = graph[current]
        for step in closed:
            if steps[step] >= minutes - minute:
                continue
            new_flow = flow + flows[step] * (minutes - minute - steps[step] - 1)
            queue.append((minute + 1 + steps[step], new_flow, step, closed - {step}))
            if new_flow > max_flow:
                max_flow = new_flow
    return max_flow

# --------------------------------------------------------------------
# PART 2 FUNCTIONS
# --------------------------------------------------------------------

def best_flow_subgraph(graph, flows, minutes, valves):
    subgraph = {
        v: {t: d for t, d in ts.items() if t in valves}
        for v, ts in graph.items()
        if v in valves or v == "AA"
    }
    subflows = {v: fr for v, fr in flows.items() if v in valves} | {"AA": 0}
    return best_flow(subgraph, subflows, minutes)

def split_valves(valves):
    rooms = {valve for valve in valves if valve != "AA"}
    size = len(rooms) // 2
    for me in itertools.combinations(sorted(rooms), size):
        yield set(me), rooms - set(me)

def part1(data):
    # DATA IS ALREADY PARSED AT THIS POINT
    return best_flow(*data, 30)

def part2(data):
    # DATA IS ALREADY PARSED AT THIS POINT
    graph, flows = data
    return max(
        best_flow_subgraph(graph, flows, minutes=26, valves=me)
        + best_flow_subgraph(graph, flows, minutes=26, valves=elephant)
        for me, elephant in split_valves(graph.keys())
    )

# --------------------------------------------------------------------
# SOLVE EACH PART (CODE WAS REFACTORED AFTER PART 2 WAS REVEALED)
# --------------------------------------------------------------------

def solve(puzzle_input):
    data = parse_data(puzzle_input)
    return part1(data), part2(data)

part1, part2 = solve(puzzle_input=data)

# --------------------------------------------------------------------
# SUBMIT ANSWER
# --------------------------------------------------------------------

submit(part1, part='a')
submit(part2, part='b')