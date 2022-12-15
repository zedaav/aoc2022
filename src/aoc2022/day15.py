import itertools
import logging
import re
from functools import lru_cache
from pathlib import Path
from typing import Set

import numpy as np

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/15
"""

# Instructions pattern
INST_PATTERN = re.compile("Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)")


# Distance reckoning function
@lru_cache
def distance(x1: int, y1: int, x2: int, y2: int):
    return abs(y2 - y1) + abs(x2 - x1)


# Puzzle class
class D15Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.sensors = {}
        self.x_min = None
        self.x_max = 0

        # Super call
        super().__init__(input_file)

        # Some logs
        logging.info(f"x span: {self.x_min} -- {self.x_max}")

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Get sensor-beacon pair
        m = INST_PATTERN.match(trimmed_line)
        x_s, y_s = int(m.group(1)), int(m.group(2))
        x_b, y_b = int(m.group(3)), int(m.group(4))
        self.x_min = x_s if self.x_min is None else min(x_s, self.x_min)
        self.x_max = max(x_s, self.x_max)
        self.sensors[(x_s, y_s)] = (x_b, y_b)

        return trimmed_line


# Step 1 class
class D15Step1Puzzle(D15Puzzle):
    def get_no_beacons_candidates(self, at_line: int) -> Set[int]:
        # Iterate on sensors
        beacons = set()
        no_beacons = set()
        for (x_s, y_s), (x_b, y_b) in self.sensors.items():
            if y_b == at_line:
                # One more beacon on this line
                beacons.add(x_b)

            # Distance between current sensor and beacon
            d = distance(x_s, y_s, x_b, y_b)

            # Reduced WRT. current line
            d -= abs(at_line - y_s)

            # Handle all positions from current x
            no_beacons.update(range(x_s - d, x_s + d + 1))

        return no_beacons - beacons

    def solve(self, at_line: int) -> int:
        # Get positions without beacons for this line
        return len(self.get_no_beacons_candidates(at_line))


# Step 2 class
class D15Step2Puzzle(D15Puzzle):
    def solve(self, max_offset: int) -> int:
        array = np.array([[a, b, c, d] for (a, b), (c, d) in self.sensors.items()])
        beacon_dist = np.abs(array[:, 0:2] - array[:, 2:4]).sum(1)
        xl, xh = np.array([0, 0]), np.array([max_offset] * 2)
        stack = [(xl, xh)]

        while True:
            xl, xh = stack.pop()
            if np.all(xl == xh):
                return xl[0] * 4_000_000 + xl[1]
            xm = (xl + xh) // 2  # Partition into up to 4 quadtree child cells.
            for child_min_max in itertools.product(*(((ll, m), (m + 1, h)) if m < h else ((ll, h),) for ll, m, h in zip(xl, xm, xh))):
                xl, xh = np.array(child_min_max).T
                dist = (np.maximum(xh - array[:, 0:2], 0) + np.maximum(array[:, 0:2] - xl, 0)).sum(1)
                if not np.any(dist <= beacon_dist):
                    stack.append((xl, xh))
