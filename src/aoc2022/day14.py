import logging
import re
from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/14
"""

# Rock line separator
ROCK_SEPARATOR = " -> "

# Rock pattern
ROCK_PATTERN = re.compile("([0-9]+),([0-9]+)")


# Puzzle class
class D14Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.rock_lines = []
        self.x_max = 500
        self.y_max = 0

        # Super call
        super().__init__(input_file)

        # Build initial map
        self.width = self.x_max
        self.height = self.y_max + 1
        self.grid = [["."] * (500 + self.width) for _ in range(self.height)]

        # Add rocks
        for rock_line in self.rock_lines:
            for (x1, y1), (x2, y2) in zip(rock_line[:-1], rock_line[1:]):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        self.grid[y][x] = "#"

    def dump_init_map(self):
        logging.info(f"Initial map ({self.width}x{self.height}")

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Grab rock lines
        new_rock_line = []
        for rock_str in trimmed_line.split(ROCK_SEPARATOR):
            m = ROCK_PATTERN.match(rock_str)
            assert m is not None
            x, y = int(m.group(1)), int(m.group(2))
            new_rock_line.append((x, y))

            # Check for table max dimensions
            self.x_max = max(self.x_max, x)
            self.y_max = max(self.y_max, y)

        self.rock_lines.append(new_rock_line)

        return trimmed_line

    def drop(self):
        x_sand, y_sand = 500, 0
        while y_sand < self.height:
            if self.grid[y_sand][x_sand] == ".":
                pass
            elif self.grid[y_sand][x_sand - 1] == ".":
                x_sand -= 1
            elif self.grid[y_sand][x_sand + 1] == ".":
                x_sand += 1
            else:
                self.grid[y_sand - 1][x_sand] = "o"
                return True
            y_sand += 1

        # Reached bottom
        return False


# Step 1 class
class D14Step1Puzzle(D14Puzzle):
    def __init__(self, input_file: Path):
        # Default map fill
        super().__init__(input_file)
        self.dump_init_map()

    def solve(self):
        # Drop sand, until reached bottom
        units_count = 0
        while self.drop():
            units_count += 1
        return units_count


# Step 2 class
class D14Step2Puzzle(D14Puzzle):
    def __init__(self, input_file: Path):
        # Default map fill
        super().__init__(input_file)

        # Append a bottom lines
        self.height += 2
        self.grid += [["."] * (500 + self.width)]  # Add bottom line
        self.grid += [["#"] * (500 + self.width)]  # Add bottom line
        self.dump_init_map()

    def solve(self):
        # Drop sand, until sand heap reach top of the cave
        units_count = 0
        while self.grid[0][500] == ".":
            self.drop()
            units_count += 1
        return units_count
