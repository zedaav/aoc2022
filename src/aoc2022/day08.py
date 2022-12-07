from pathlib import Path
from typing import Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/8
"""


# Puzzle class
class D08Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        return parsed_line

    def solve(self) -> Union[int, str]:
        # Solution is...
        return 0


# Step 1 class
class D08Step1Puzzle(D08Puzzle):
    pass


# Step 2 class
class D08Step2Puzzle(D08Puzzle):
    pass
