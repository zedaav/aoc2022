from pathlib import Path
from typing import Set, Tuple

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/18
"""


# Puzzle class
class D18Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.cubes = set()
        self.droplet_span = 0

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Split on comma to build the new cube tuple
        new_cube = tuple(int(c) for c in trimmed_line.split(","))
        self.cubes.add(new_cube)

        # Update containing cube dimension
        for x in new_cube:
            self.droplet_span = max(self.droplet_span, x)

        return trimmed_line

    def get_neighbors(self, x: int, y: int, z: int) -> Set[Tuple]:
        # Get neighbors cubes for required one
        return {(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)}


# Step 1 class
class D18Step1Puzzle(D18Puzzle):
    def solve(self) -> int:
        # Just count cubes that are not neighbors of any cube
        return sum((n not in self.cubes) for c in self.cubes for n in self.get_neighbors(*c))


# Step 2 class
class D18Step2Puzzle(D18Puzzle):
    def solve(self) -> int:
        # Find all cubes on on exterior of the droplet
        exterior_cubes = set()
        todo = [(-1, -1, -1)]
        while len(todo):
            # Next cube
            current = todo.pop()
            exterior_cubes.add(current)

            # Stack cubes that are:
            # - neighbors of the current one
            # - in cube range (no need to go too far)
            # - but not in the exterior_cubes list
            # - and not a known cube
            todo += [s for s in (self.get_neighbors(*current) - self.cubes - exterior_cubes) if all(-1 <= x <= (self.droplet_span + 1) for x in s)]

        # Count exterior cubes adjacent to the droplet
        return sum((n in exterior_cubes) for c in self.cubes for n in self.get_neighbors(*c))
