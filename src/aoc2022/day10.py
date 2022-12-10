import logging
from pathlib import Path
from typing import Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/10
"""

# Instructions prefixes
INST_ADD = "addx "
INST_NOP = "noop"


# Puzzle class
class D10Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.current_value = 1
        self.values = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Check instruction
        if trimmed_line.startswith(INST_NOP):
            # Just add one cycle with same value
            self.values.append(self.current_value)
        else:
            # Add two cycles with previous values, then change value
            self.values.append(self.current_value)
            self.values.append(self.current_value)
            self.current_value += int(trimmed_line[len(INST_ADD) :])

        return trimmed_line


# Step 1 class
class D10Step1Puzzle(D10Puzzle):
    def solve(self) -> Union[int, str]:
        # Sample values
        result = 0
        for sample in [20, 60, 100, 140, 180, 220]:
            register = self.values[sample - 1]
            logging.info(f"Register value at cycle {sample}: {register}")
            result += register * sample
        return result


# Step 2 class
class D10Step2Puzzle(D10Puzzle):
    def solve(self) -> Union[int, str]:
        # Render image
        line_length = 40
        rendered_line = ""
        output = []
        for cycle in range(240):
            # Is register matching cycle position?
            register = self.values[cycle]
            sprite_left = register - 1
            sprite_right = register + 1
            pixel = cycle % line_length  # NOQA: S001
            if (pixel >= sprite_left) and (pixel <= sprite_right):
                rendered_line += "#"
            else:
                rendered_line += "."

            # One more line?
            if (cycle % line_length) == (line_length - 1):  # NOQA: S001
                output.append(rendered_line)
                logging.info(f"Rendered line: {rendered_line}")
                rendered_line = ""

        return output
