import logging
from pathlib import Path

import numpy as np

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/17
"""

# Tower and shapes are handled with 1D array of numbers
#
# ...
# 14 15 16 17 18 19 20
#  7  8  9 10 11 12 13
#  0  1  2  3  4  5  6

# Shapes
SHAPES = [
    np.array([2, 3, 4, 5], dtype=int),  # "-" horizontal bar
    np.array([3, 9, 10, 11, 17], dtype=int),  # "+" sign
    np.array([2, 3, 4, 11, 18], dtype=int),  # Reversed "L" sign
    np.array([2, 9, 16, 23], dtype=int),  # "|" vertical bar
    np.array([2, 3, 9, 10], dtype=int),  # Square
]


# Puzzle class
class D17Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.jet_instructions = None

        # Super call
        super().__init__(input_file)

        # Count of jet instructions
        self.jet_count = len(self.jet_instructions)
        self.jet_next = 0

        # Count of shapes
        self.shape_count = len(SHAPES)
        self.shape_next = 0

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Get instructions
        self.jet_instructions = trimmed_line

        return trimmed_line

    # Fetching next jet instruction (looping on input instructions)
    def get_next_jet(self) -> str:
        to_ret = self.jet_instructions[self.jet_next]
        self.jet_next = (self.jet_next + 1) % self.jet_count
        return to_ret

    # Fetching next shape (looping on available shapes)
    def get_next_shape(self) -> str:
        to_ret = SHAPES[self.shape_next]
        self.shape_next = (self.shape_next + 1) % self.shape_count
        return to_ret

    def build(self, count: int) -> int:
        # Iterate on rocks count
        tower = np.array([], dtype=int)
        tower_height = 0
        tower_baseline = 0
        known_situations = set()
        repeat_pattern = 0
        first_repeat_baseline = 0
        rock_nb = -1
        while True:
            # Next rock
            rock_nb += 1
            if rock_nb >= count:
                # Ok, end of the loop
                break

            # Forget rocks below the "sky line"
            if rock_nb:
                all_max = []
                for c in range(7):
                    rocks_in_c = tower[np.where(tower % 7 == c)]
                    if len(rocks_in_c):
                        all_max.append(rocks_in_c.max() // 7)

                # Keep only rocks above the lowest max (- 5 lines for some margin)
                new_baseline = min(all_max) - 5
                if (len(all_max) == 7) and (new_baseline > 0):
                    tower = tower[np.where(tower >= new_baseline * 7)] - new_baseline * 7
                    tower_baseline += new_baseline

                # New tower height
                tower_height = (tower.max() // 7) + 1

            # Isn't that something we've already seen? (next jet, next rock, sky line)
            # (Only check if not already done)
            if repeat_pattern < 2:
                situation = (self.jet_next, self.shape_next, tuple(tower))
                if situation not in known_situations:
                    known_situations.add(situation)
                else:
                    # Yes it is!
                    situations_count = len(known_situations)
                    logging.info(f"Repeating pattern found after {rock_nb} rocks at height {tower_baseline} (known situations: {situations_count})")
                    if repeat_pattern == 0:
                        # First time, just reset because there may be some iteration before getting the repeating pattern to appear
                        known_situations.clear()
                        known_situations.add(situation)
                        repeat_pattern += 1
                        first_repeat_baseline = tower_baseline
                    else:
                        # Second time, we can skip the next N iterations
                        skip_count = (count - rock_nb) // situations_count
                        logging.info(f"Skipping {skip_count} iterations")

                        rock_nb += skip_count * situations_count
                        tower_baseline += skip_count * (tower_baseline - first_repeat_baseline)
                        repeat_pattern += 1

            # Get next shape, 3 steps above of the tower highest piece
            shape = self.get_next_shape() + (tower_height + 3) * 7

            # Loop until we intersect with the tower
            while True:
                # Jet instruction
                h_offset = +1 if (self.get_next_jet() == ">") else -1

                # On the border?
                if ((h_offset < 0) and not np.any(shape % 7 == 0)) or ((h_offset > 0) and not np.any(shape % 7 == 6)):
                    # No, tentative to shift left/right
                    tentative_shape = shape + h_offset
                    if not len(np.intersect1d(tentative_shape, tower)):
                        # Not overlapping with tower rocks as well, shift is ok
                        shape = tentative_shape

                # Tentative to fall down
                tentative_shape = shape - 7

                # Negative height or intersect with existing tower means that it actually can't fall down
                if np.any(tentative_shape < 0) or len(np.intersect1d(tentative_shape, tower)):
                    # Add shape to tower
                    tower = np.append(tower, shape)
                    break
                else:
                    # Can fall down, remember new shape position
                    shape = tentative_shape

        # Solution is tower height
        return (tower.max() // 7) + 1 + tower_baseline


# Step 1 class
class D17Step1Puzzle(D17Puzzle):
    def solve(self) -> int:
        return self.build(2022)


# Step 2 class
class D17Step2Puzzle(D17Puzzle):
    def solve(self) -> int:
        # See https://www.reddit.com/r/adventofcode/comments/znykq2/comment/j0lxz9y/?utm_source=share&utm_medium=web2x&context=3
        return self.build(1000000000000)
