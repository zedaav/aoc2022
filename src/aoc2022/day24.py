import logging
from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/24
"""


# Puzzle class
class D24Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.blizzards = []

        # Super call
        super().__init__(input_file)

        # Number of possible blizzard positions
        self.width = len(self.input_lines[0]) - 2
        self.height = len(self.input_lines) - 2
        logging.info(f"Grid size: {self.width} x {self.height}")
        logging.info(f"Initial blizzards positions: {self.blizzards}")
        self.start = (-1, 0)
        self.stop = (self.height, self.width - 1)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Get blizzards positions
        if trimmed_line[2] != "#":
            self.blizzards.append(trimmed_line[1:-1])

        return trimmed_line

    def resolve(self, start, stop, step=1) -> int:
        # Initial position
        positions = {start}

        # Loop until stop position is reached
        while True:
            # Find new_positions for this step
            new_positions = set()
            for y, x in positions:
                for ny, nx in [(y, x), (y - 1, x), (y + 1, x), (y, x + 1), (y, x - 1)]:
                    # Stop position?
                    if (ny, nx) == stop:
                        return step

                    # New position not matching with a blizzard?
                    if (
                        (0 <= nx < self.width)
                        and (0 <= ny < self.height)
                        and self.blizzards[ny][(nx - step) % self.width] != ">"
                        and self.blizzards[ny][(nx + step) % self.width] != "<"
                        and self.blizzards[(ny - step) % self.height][nx] != "v"
                        and self.blizzards[(ny + step) % self.height][nx] != "^"
                    ):
                        # This is a valid new position
                        new_positions.add((ny, nx))

            # Get ready for next round
            positions = new_positions
            if not len(positions):
                positions.add(start)
            step += 1


# Step 1 class
class D24Step1Puzzle(D24Puzzle):
    def solve(self) -> int:
        return self.resolve(self.start, self.stop)


# Step 2 class
class D24Step2Puzzle(D24Puzzle):
    def solve(self) -> int:
        return self.resolve(self.start, self.stop, self.resolve(self.stop, self.start, self.resolve(self.start, self.stop)))
