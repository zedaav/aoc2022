import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import mip

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/19
"""

# Instruction pattern
BLUEPRINT_PATTERN = re.compile(
    "Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian."
)


# Blueprint m
@dataclass
class BluePrint:
    bp_id: int
    ore_cost: int
    clay_cost: int
    obs_cost: Tuple[int, int]
    geode_cost: Tuple[int, int]


# Find max geodes for a given blueprint
def get_max_geodes(bp: BluePrint, minutes: int) -> int:
    # Setup model
    m = mip.Model(sense=mip.MAXIMIZE)

    # Objective
    obj = mip.LinExpr(0)

    # Keep variables indexed by minutes
    vars_all = []
    for target_minute in range(minutes):
        # Build variables to track resources
        current_vars = {}
        current_vars.update({"ore": m.add_var(f"ore_{target_minute}", var_type=mip.BINARY)})
        current_vars.update({"clay": m.add_var(f"clay_{target_minute}", var_type=mip.BINARY)})
        current_vars.update({"obs": m.add_var(f"obs_{target_minute}", var_type=mip.BINARY)})
        current_vars.update({"geo": m.add_var(f"geo_{target_minute}", var_type=mip.BINARY)})
        vars_all.append(current_vars)

        m.add_constr(current_vars["ore"] + current_vars["clay"] + current_vars["obs"] + current_vars["geo"] <= 1)

        # Resources expressions
        ore = mip.LinExpr(const=target_minute)
        clay = mip.LinExpr(const=0)
        obs = mip.LinExpr(const=0)
        for current_minute in range(target_minute):
            ore.add_var(vars_all[current_minute]["ore"], target_minute - current_minute - 1)  # Ore gain for each harvest
            ore.add_var(vars_all[current_minute]["ore"], -bp.ore_cost)  # Ore cost to build an ore robot
            ore.add_var(vars_all[current_minute]["clay"], -bp.clay_cost)  # Ore cost to build a clay robot
            ore.add_var(vars_all[current_minute]["obs"], -bp.obs_cost[0])  # Ore cost to build an obsidian robot
            ore.add_var(vars_all[current_minute]["geo"], -bp.geode_cost[0])  # Ore cost to build a geode robot

            clay.add_var(vars_all[current_minute]["clay"], target_minute - current_minute - 1)  # Clay gain for each harvest
            clay.add_var(vars_all[current_minute]["obs"], -bp.obs_cost[1])  # Clay cost to build an obsidian robot

            obs.add_var(vars_all[current_minute]["obs"], target_minute - current_minute - 1)  # Obsidian gain for each harvest
            obs.add_var(vars_all[current_minute]["geo"], -bp.geode_cost[1])  # Obsidian cost to build a geode robot

        # Constraints
        m.add_constr(
            ore
            >= current_vars["ore"] * bp.ore_cost
            + current_vars["clay"] * bp.clay_cost
            + current_vars["obs"] * bp.obs_cost[0]
            + current_vars["geo"] * bp.geode_cost[0]
        )
        m.add_constr(clay >= current_vars["obs"] * bp.obs_cost[1])
        m.add_constr(obs >= current_vars["geo"] * bp.geode_cost[1])

        obj.add_var(current_vars["geo"], minutes - target_minute - 1)

    m.objective = obj

    m.optimize()

    return int(m.objective_value)


# Puzzle class
class D19Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.blueprints = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Parse line
        m = BLUEPRINT_PATTERN.match(trimmed_line)
        assert m is not None
        self.blueprints.append(
            BluePrint(int(m.group(1)), int(m.group(2)), int(m.group(3)), (int(m.group(4)), int(m.group(5))), (int(m.group(6)), int(m.group(7))))
        )

        return trimmed_line


# Step 1 class
class D19Step1Puzzle(D19Puzzle):
    def solve(self) -> int:
        # Sum qualities
        return sum(get_max_geodes(bp, 24) * bp.bp_id for bp in self.blueprints)


# Step 2 class
class D19Step2Puzzle(D19Puzzle):
    def solve(self) -> int:
        # Multiply max of the first 3 blueprints
        result = 1
        for val in [get_max_geodes(bp, 32) for bp in (self.blueprints if len(self.blueprints) < 3 else self.blueprints[:3])]:
            result *= val
        return result
