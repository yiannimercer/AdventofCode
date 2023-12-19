from aocd import get_data, submit
from dotenv import load_dotenv
from heapq import *

load_dotenv()

# --------------------------------------------------------------------
# READ DATA IN
# --------------------------------------------------------------------

map_data = get_data(day=17, year=2023).splitlines()

example_data = ['2413432311323',
                '3215453535623',
                '3255245654254',
                '3446585845452',
                '4546657867536',
                '1438598798454',
                '4457876987766',
                '3637877979653',
                '4654967986887',
                '4564679986453',
                '1224686865563',
                '2546548887735',
                '4322674655533']

# --------------------------------------------------------------------
# PART 1
# --------------------------------------------------------------------


def min_heat_path(map_data) -> None:

    width = len(map_data[0])
    height = len(map_data)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    heap = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    seen = set()

    while len(heap) > 0:
        heat, x, y, direction, streak = heappop(heap)

        if (x, y, direction, streak) in seen:
            continue

        seen.add((x, y, direction, streak))

        if x == width - 1 and y == height - 1:
            print(heat)
            return heat

        dx, dy = directions[direction]
        x += dx
        y += dy

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        heat += int(map_data[y][x])


        if streak < 2:
            heappush(heap, (heat, x, y, direction, streak + 1))

        heappush(heap, (heat, x, y, (direction + 1) % 4, 0))
        heappush(heap, (heat, x, y, (direction - 1) % 4, 0))
        
        
min_heat = min_heat_path(map_data)

# --------------------------------------------------------------------
# PART 2
# --------------------------------------------------------------------


def min_heat_path_part2(map_data) -> None:
    
    width = len(map_data[0])
    height = len(map_data)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    heap = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    seen = set()

    while len(heap) > 0:
        heat, x, y, direction, streak = heappop(heap)

        if (x, y, direction, streak) in seen:
            continue

        seen.add((x, y, direction, streak))

        if x == width - 1 and y == height - 1:
            if streak > 3:
                print(heat)
                return heat

        dx, dy = directions[direction]
        x += dx
        y += dy

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        heat += int(map_data[y][x])


        if streak < 10:
            heappush(heap, (heat, x, y, direction, streak))

        if streak > 3:
            heappush(heap, (heat, x, y, (direction + 1) % 4, 0))
            heappush(heap, (heat, x, y, (direction - 1) % 4, 0))


min_heat_part2 = min_heat_path_part2(map_data)

submit(min_heat, part='a', day=17, year=2023)