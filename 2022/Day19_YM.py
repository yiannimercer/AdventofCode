from dotenv import load_dotenv

load_dotenv()
from aocd import get_data, submit
from parse import parse
from math import inf, prod
import mip as mip

# --------------------------------------------------------------------
# DAY 19 INPUT DATA
# --------------------------------------------------------------------

data = get_data(day=19).split("\n")

# --------------------------------------------------------------------
# PARSE INPUT DATA
# --------------------------------------------------------------------


def parse_blueprint(data_line):
    data_line = "".join(data_line.splitlines())
    template = "Blueprint {id}: Each ore robot costs {ore_robot_cost} ore. Each clay robot costs {clay_robot_cost} ore. Each obsidian robot costs {obsidian_robot_cost_ore} ore and {obsidian_robot_cost_clay} clay. Each geode robot costs {geode_cost_ore} ore and {geode_robot_cost_obsidian} obsidian."
    blueprint_dict = parse(template, data_line).named
    return blueprint_dict


blueprints = []
for blueprint in data:
    values = parse_blueprint(blueprint)
    blueprints.append({k: int(v) for k, v in values.items()})

# --------------------------------------------------------------------
# CREATE OPTIMIZATION MODEL AND RUN WITH EACH BLUEPRINT
# --------------------------------------------------------------------


def optimize_blueprint(total_minutes, blueprint, part):
    model = mip.Model(sense=mip.MAXIMIZE)
    obj = mip.LinExpr(0)
    all_resources = []

    # ITERATE THROUGH THE TOTAL ALLOWED TIME
    for min in range(total_minutes):
        resources = {}
        resources.update({"ore": model.add_var(f"ore_{min}", var_type=mip.BINARY)})
        resources.update({"clay": model.add_var(f"clay_{min}", var_type=mip.BINARY)})
        resources.update(
            {"obsidian": model.add_var(f"obsidian_{min}", var_type=mip.BINARY)}
        )
        resources.update({"geode": model.add_var(f"geode_{min}", var_type=mip.BINARY)})
        all_resources.append(resources)

        model.add_constr(
            resources["ore"]
            + resources["clay"]
            + resources["obsidian"]
            + resources["geode"]
            <= 1
        )

        # COST OF ROBOTS FOR DIFFERENT RESOURCES
        ore = mip.LinExpr(const=min)
        clay = mip.LinExpr(const=0)
        obsidian = mip.LinExpr(const=0)

        # ADD HOW MUCH RESOURCES CURRENT ROBOT WILL COLLECT
        for m_ in range(min):
            # ORE
            ore.add_var(all_resources[m_]["ore"], min - m_ - 1)
            ore.add_var(all_resources[m_]["ore"], -blueprint["ore_robot_cost"])
            ore.add_var(all_resources[m_]["clay"], -blueprint["clay_robot_cost"])
            ore.add_var(
                all_resources[m_]["obsidian"], -blueprint["obsidian_robot_cost_ore"]
            )
            ore.add_var(all_resources[m_]["geode"], -blueprint["geode_cost_ore"])

            # CLAY
            clay.add_var(all_resources[m_]["clay"], min - m_ - 1)
            clay.add_var(
                all_resources[m_]["obsidian"], -blueprint["obsidian_robot_cost_clay"]
            )

            # OBSIDIAN
            obsidian.add_var(all_resources[m_]["obsidian"], min - m_ - 1)
            obsidian.add_var(
                all_resources[m_]["geode"], -blueprint["geode_robot_cost_obsidian"]
            )

        # ADD ROBOT COST CONSTRAINTS
        model.add_constr(
            ore
            >= resources["ore"] * blueprint["ore_robot_cost"]
            + resources["clay"] * blueprint["clay_robot_cost"]
            + resources["obsidian"] * blueprint["obsidian_robot_cost_ore"]
            + resources["geode"] * blueprint["geode_cost_ore"]
        )
        model.add_constr(
            clay >= resources["obsidian"] * blueprint["obsidian_robot_cost_clay"]
        )
        model.add_constr(
            obsidian >= resources["geode"] * blueprint["geode_robot_cost_obsidian"]
        )

        # ADD THE GEODE VARIABLE TO OBJECTIVE
        obj.add_var(resources["geode"], total_minutes - min - 1)

    # SET MODEL OBJECTIVE TO BE GEODES WITH GOAL IS TO MAXIMIZE
    model.objective = obj
    # WRITE MODEL OUT
    if part == 1:
        model.write(f"./Day19 Models/AOCD_DAY19_{blueprint['id']}.lp")
    else:
        model.write(f"./Day19 Models/AOCD_DAY19_{blueprint['id']}_Part2.lp")
    # OPTIMIZE BLUEPRINT MODEL
    model.optimize()
    collected_geodes = model.objective_value
    # RETURN NUMBER OF COLLECTED GEODES
    return collected_geodes


# --------------------------------------------------------------------
# PART 1 SOLVE
# --------------------------------------------------------------------

quality_levels_p1 = []
for blueprint in blueprints:
    collected_geodes = optimize_blueprint(24, blueprint, 1)
    quality_lvl = collected_geodes * blueprint["id"]
    quality_levels_p1.append(quality_lvl)
part1 = int(sum(quality_levels_p1))
print(f"Part 1: {part1}")
submit(part1, part="a")

# --------------------------------------------------------------------
# PART 2 SOLVE
# --------------------------------------------------------------------

quality_levels_p2 = []
first_three = blueprints[:3]
for blueprint in first_three:
    collected_geodes = optimize_blueprint(32, blueprint, 2)
    quality_levels_p2.append(collected_geodes)
part2 = int(quality_levels_p2[0] * quality_levels_p2[1] * quality_levels_p2[2])
print(f"Part 2: {part2}")
submit(part2, part="b")
