import re
from aocd import get_data, submit
from dotenv import load_dotenv

load_dotenv()

#############
# GET DATA #
############

data = get_data(day=2, year=2023).splitlines()

##########
# PART 1 #
##########

# Create dictionary in the below form
# {Game #: "red_counts": R, "green_counts": B, ...}


# Populate Dict with Regex Counts & Sums
games_list = {
    int(re.findall(r"Game (\d+)", game)[0]): {
        "green_counts": ([int(num) for num in re.findall(r"(\d+) green", game)]),
        "red_counts": ([int(num) for num in re.findall(r"(\d+) red", game)]),
        "blue_counts": ([int(num) for num in re.findall(r"(\d+) blue", game)]),
    }
    for game in data
}

# Filter dict where conditions are true
filters = {"red": 12, "green": 13, "blue": 14}
possible_games = []
for game_num, game_counts in games_list.items():
    if (
        all(green <= filters["green"] for green in game_counts["green_counts"])
        and all(red <= filters["red"] for red in game_counts["red_counts"])
        and all(blue <= filters["blue"] for blue in game_counts["blue_counts"])
    ):
        possible_games.append(game_num)

part1_answer = sum(possible_games)
submit(part1_answer, part="a", day=2, year=2023)


##########
# PART 2 #
##########

# Need to change the games_list to grab the max of each color for each game as this represents the min peices you need to play
games_list_max = {
    int(re.findall(r"Game (\d+)", game)[0]): {
        "green_min": max([int(num) for num in re.findall(r"(\d+) green", game)]),
        "red_min": max([int(num) for num in re.findall(r"(\d+) red", game)]),
        "blue_min": max([int(num) for num in re.findall(r"(\d+) blue", game)]),
    }
    for game in data
}

# Calculate power of each game

game_powers = []
for game_num, game_counts in games_list_max.items():
    game_power = (
        game_counts["green_min"] * game_counts["red_min"] * game_counts["blue_min"]
    )
    game_powers.append(game_power)

part2_answer = sum(game_powers)
submit(part2_answer, part="b", day=2, year=2023)
