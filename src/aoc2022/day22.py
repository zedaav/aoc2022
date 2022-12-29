import logging
import re
from abc import abstractmethod
from enum import IntEnum
from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/22
"""

# Hard-coded dimensions for sample/input (too lazy to find them dynamically)
SAMPLE_SIZE = 4
SAMPLE_SPAN_Y = 3
INPUT_SIZE = 50


# Enum for directions
class Dir(IntEnum):
    E = 0  # East
    S = 1  # South
    W = 2  # West
    N = 3  # North


# Puzzle class
class D22Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Setup data
        self.grid_lines = []
        self.instructions = ""

        # Super call
        super().__init__(input_file)

        # Check dimensions
        if len(self.grid_lines) == SAMPLE_SIZE * SAMPLE_SPAN_Y:
            self.size = SAMPLE_SIZE
        else:
            self.size = INPUT_SIZE

        # Build grid (all positions of empty spaces and walls)
        self.grid = {(x, y): c for y, r in enumerate(self.grid_lines) for x, c in enumerate(r) if c in ".#"}
        logging.info(f"Parsed instructions: {self.instructions}")

        # Min/max
        self.x0, self.y0 = min(x for x, y in self.grid.keys()), min(y for x, y in self.grid.keys())
        self.x1, self.y1 = max(x for x, y in self.grid.keys()), max(y for x, y in self.grid.keys())

    def parse_line(self, index: int, line: str) -> str:
        trimmed_line = line.strip("\r\n")
        if len(trimmed_line):
            if trimmed_line[0] in " .#":
                self.grid_lines.append(trimmed_line)
            else:
                self.instructions = re.findall("L|R|\\d+", trimmed_line)

    def solve(self) -> int:
        # Initial positions
        y, x = min((k[1], k[0]) for k, v in self.grid.items() if v == ".")
        aim = Dir.E

        # Iterate on instructions
        for i in self.instructions:
            if i == "L":
                # Turn left
                aim = Dir((aim.value - 1) % 4)
            elif i == "R":
                # Turn right
                aim = Dir((aim.value + 1) % 4)
            else:
                # Walk on the required distance
                x, y, aim = self.update_pos(int(i), x, y, aim)

        # Final password reckoning
        return 1000 * (y + 1) + 4 * (x + 1) + aim.value

    @abstractmethod
    def update_pos(self, distance: int, x: int, y: int, aim: Dir):  # pragma: no cover
        pass


# Step 1 class
class D22Step1Puzzle(D22Puzzle):
    def update_pos(self, distance: int, x: int, y: int, aim: Dir):
        # Delta x/y
        dx = [1, 0, -1, 0][aim.value]
        dy = [0, 1, 0, -1][aim.value]

        # Iterate on distance
        for _s in range(distance):
            # New position candidate
            nx, ny = x + dx, y + dy

            # If out of grid, loop until we get back in it
            while (nx, ny) not in self.grid:
                nx += dx
                ny += dy
                if nx < self.x0:
                    nx = self.x1
                if nx > self.x1:
                    nx = self.x0
                if ny < self.y0:
                    ny = self.y1
                if ny > self.y1:
                    ny = self.y0

            # Candidate is empty space: update position
            if self.grid[(nx, ny)] == ".":
                x, y = nx, ny
            # Candidate is a wall, stop here
            elif self.grid[(nx, ny)] == "#":  # pragma: no branch
                break

        return x, y, aim


# Step 2 class
class D22Step2Puzzle(D22Puzzle):
    def update_pos(self, distance: int, x: int, y: int, aim: Dir):
        for _s in range(distance):
            # Delta x/y
            dx = [1, 0, -1, 0][aim.value]
            dy = [0, 1, 0, -1][aim.value]

            # New position candidate
            nx, ny, n_aim = x + dx, y + dy, aim

            # Out of grid?
            if (nx, ny) not in self.grid:
                # Current cube face
                ox, oy = x // self.size, y // self.size

                # Next cube face
                fx, fy = nx // self.size, ny // self.size

                # Remaining part
                rx, ry = nx % self.size, ny % self.size  # NOQA:S001
                if (ox, oy) == (1, 0):
                    if (fx, fy) == (1, -1):
                        fx, fy = 0, 3
                        rx, ry = (self.size - 1) - ry, rx
                        n_aim = Dir.E
                    if (fx, fy) == (0, 0):
                        fx, fy = 0, 2
                        rx, ry = (self.size - 1) - rx, (self.size - 1) - ry
                        n_aim = Dir.E
                elif (ox, oy) == (2, 0):
                    if (fx, fy) == (2, -1):
                        fx, fy = 0, 3
                        n_aim = aim
                    elif (fx, fy) == (3, 0):
                        fx, fy = 1, 2
                        rx, ry = (self.size - 1) - rx, (self.size - 1) - ry
                        n_aim = Dir.W
                    elif (fx, fy) == (2, 1):  # pragma: no branch
                        fx, fy = 1, 1
                        rx, ry = (self.size - 1) - ry, rx
                        n_aim = Dir.W
                elif (ox, oy) == (1, 1):
                    if (fx, fy) == (0, 1):
                        fx, fy = 0, 2
                        rx, ry = ry, (self.size - 1) - rx
                        n_aim = Dir.S
                    elif (fx, fy) == (2, 1):  # pragma: no branch
                        fx, fy = 2, 0
                        rx, ry = ry, (self.size - 1) - rx
                        n_aim = Dir.N
                elif (ox, oy) == (0, 2):
                    if (fx, fy) == (0, 1):
                        fx, fy = 1, 1
                        rx, ry = (self.size - 1) - ry, rx
                        n_aim = Dir.E
                    elif (fx, fy) == (-1, 2):  # pragma: no branch
                        fx, fy = 1, 0
                        rx, ry = (self.size - 1) - rx, (self.size - 1) - ry
                        n_aim = Dir.E
                elif (ox, oy) == (1, 2):
                    if (fx, fy) == (2, 2):
                        fx, fy = 2, 0
                        rx, ry = (self.size - 1) - rx, (self.size - 1) - ry
                        n_aim = Dir.W
                    elif (fx, fy) == (1, 3):  # pragma: no branch
                        fx, fy = 0, 3
                        rx, ry = (self.size - 1) - ry, rx
                        n_aim = Dir.W
                elif (ox, oy) == (0, 3):  # pragma: no branch
                    if (fx, fy) == (-1, 3):
                        fx, fy = 1, 0
                        rx, ry = ry, (self.size - 1) - rx
                        n_aim = Dir.S
                    elif (fx, fy) == (1, 3):
                        fx, fy = 1, 2
                        rx, ry = ry, (self.size - 1) - rx
                        n_aim = Dir.N
                    elif (fx, fy) == (0, 4):  # pragma: no branch
                        fx, fy = 2, 0
                        n_aim = aim

                # Update candidate after cube face switch
                nx, ny = fx * self.size + rx, fy * self.size + ry

            # Free space, ok to update
            if self.grid[(nx, ny)] == ".":
                x, y, aim = nx, ny, n_aim
            # Wall, stop here
            elif self.grid[(nx, ny)] == "#":  # pragma: no branch
                break

        return x, y, aim
