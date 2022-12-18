from pathlib import Path
from typing import Union

from sortedcontainers import SortedDict

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/18
"""


# Puzzle class
class D18Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.cubes = []
        self.sorted_cubes = [SortedDict() for _ in range(3)]

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Split on comma
        new_cube = [int(c) for c in trimmed_line.split(",")]
        self.cubes.append(new_cube)

        # Contribute on sorted dicts for each axis
        for x in range(3):
            key = new_cube[x]
            if key not in self.sorted_cubes[x]:
                self.sorted_cubes[x][key] = []
            self.sorted_cubes[x][key].append(new_cube)

        return trimmed_line


# Step 1 class
class D18Step1Puzzle(D18Puzzle):
    def solve(self) -> Union[int, str]:
        # Count cubes
        cubes_count = len(self.cubes)

        # Iterate to find adjacent faces
        adjacent_faces_count = 0

        # Do it on each axis
        for axis in range(3):
            # Filter consecutive values on this axis
            axis_keys = self.sorted_cubes[axis].keys()
            for value, next_value in filter(lambda t: t[0] + 1 == t[1], zip(axis_keys[:-1], axis_keys[1:])):
                # Find cubes that are equals on the other axis between the two sets
                for c in self.sorted_cubes[axis][value]:
                    next_c = list(c)
                    next_c[axis] = next_value
                    if next_c in self.sorted_cubes[axis][next_value]:
                        adjacent_faces_count += 1

        return (cubes_count * 6) - (adjacent_faces_count * 2)


# Step 2 class
class D18Step2Puzzle(D18Puzzle):
    pass
