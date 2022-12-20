from pathlib import Path
from typing import Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/21
"""


# Puzzle class
class D21Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        return trimmed_line

    def solve(self) -> Union[int, str]:
        # Solution is...
        return 0


# Step 1 class
class D21Step1Puzzle(D21Puzzle):
    pass


# Step 2 class
class D21Step2Puzzle(D21Puzzle):
    pass
