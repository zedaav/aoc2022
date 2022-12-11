import logging
import re
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/9
"""

# Move instruction pattern
MOVE_PATTERN = re.compile("([RLDU]) +([0-9]+)")


@dataclass
class RopeKnot:
    x: int = 0
    y: int = 0

    def move(self, direction: str):
        # Move according to required direction
        if direction == "R":
            # Right
            self.x += 1
        elif direction == "L":
            # Left
            self.x -= 1
        elif direction == "U":
            # Down
            self.y += 1
        else:
            # Up
            self.y -= 1

    def follow(self, other):
        # Same position: nothing to do
        if self.x == other.x and self.y == other.y:
            return
        diff_x = other.x - self.x
        diff_y = other.y - self.y

        # Same y?
        if self.y == other.y:
            # Need to move?
            if abs(diff_x) > 1:
                self.x += 1 if (diff_x > 0) else -1

        # Same x?
        elif self.x == other.x:
            # Need to move?
            if abs(diff_y) > 1:
                self.y += 1 if (diff_y > 0) else -1

        # Last case: diagonal
        else:
            # Need to move
            if (abs(diff_x) > 1) or (abs(diff_y) > 1):
                self.x += 1 if (diff_x > 0) else -1
                self.y += 1 if (diff_y > 0) else -1


# Puzzle class
class D09Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.head = RopeKnot()
        self.knots = []
        for _ in range(self.rope_length):
            self.knots.append(RopeKnot())
        self.tail_positions = set()

        # Super call
        super().__init__(input_file)

    @property
    @abstractmethod
    def rope_length(self) -> int:  # pragma: no cover
        pass

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Parse move instruction
        m = MOVE_PATTERN.match(trimmed_line)
        assert m is not None

        # Iterate on moves number
        for _ in range(int(m.group(2))):
            # Move head in the required direction
            self.head.move(m.group(1))

            # Make knots follow
            for knot, previous_knot in zip(self.knots, [self.head] + self.knots[:-1]):
                knot.follow(previous_knot)

            # Remember tail position
            tail = self.knots[-1]
            self.tail_positions.add((tail.x, tail.y))

        logging.info(f"Positions after move: head={self.head.x},{self.head.y} tail={tail.x},{tail.y}")

        return trimmed_line

    def solve(self) -> int:
        # Solution is count of tail positions
        return len(self.tail_positions)


# Step 1 class
class D09Step1Puzzle(D09Puzzle):
    @property
    def rope_length(self) -> int:
        return 1


# Step 2 class
class D09Step2Puzzle(D09Puzzle):
    @property
    def rope_length(self) -> int:
        return 9
