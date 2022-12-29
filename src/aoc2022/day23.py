import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/23
"""


# Puzzle class
class D23Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Super call
        super().__init__(input_file)

        # Initialize elves positions
        self.elves = {(x, y) for y, line in enumerate(self.input_lines) for x, c in enumerate(line) if c == "#"}

        # Proposed directions
        self.directions = numpy.array(
            [
                [[-1, -1], [0, -1], [1, -1]],  # North
                [[-1, 1], [0, 1], [1, 1]],  # South
                [[-1, -1], [-1, 0], [-1, 1]],  # West
                [[1, -1], [1, 0], [1, 1]],  # East
            ]
        )

    def propose_move(self, elf: Tuple[int, int], proposed_moves: Dict[Tuple[int, int], List[Tuple[int, int]]]) -> bool:
        # Iterate on directions
        target = None
        alone = True
        for direction in self.directions:
            # Reckon new positions for all candidates
            candidates = elf + direction
            for candidate in candidates:
                if tuple(candidate) in self.elves:
                    # Already an elf in this candidate position
                    alone = False
                    break
            else:
                # This direction is OK
                if target is None:
                    target = tuple(candidates[1])

        # Found a target proposal?
        if not alone and target is not None:
            if target not in proposed_moves:
                proposed_moves[target] = []
            proposed_moves[target].append(elf)
            return True
        return False

    def run(self) -> bool:
        # Perform a run, and return true if something has moved

        # Iterate on elves to get proposed moves
        proposed_moves = {}
        need_to_move = False
        for elf in self.elves:
            if self.propose_move(elf, proposed_moves):
                # At lest one elf has moved
                need_to_move = True

        # No move: nothing to do
        if not need_to_move:
            return False

        # Check all proposed moves
        for proposal, elf in proposed_moves.items():
            if len(elf) > 1:
                # 2 or more elves targetting this location: don't move
                continue

            # Forget previous elf position
            self.elves.remove(elf[0])

            # ... and remember the new one
            self.elves.add(proposal)

        # Roll directions for next run
        self.directions = numpy.roll(self.directions, -1, axis=0)

        return True

    def bounds(self):
        # Check grid limits
        lo_x = float("inf")
        lo_y = float("inf")
        hi_x = float("-inf")
        hi_y = float("-inf")
        for x, y in self.elves:
            lo_x = min(lo_x, x)
            lo_y = min(lo_y, y)
            hi_x = max(hi_x, x)
            hi_y = max(hi_y, y)
        return lo_x, lo_y, hi_x, hi_y

    def draw(self):
        logging.info(" ---- elves dump ----")
        lo_x, lo_y, hi_x, hi_y = self.bounds()
        for y in range(lo_y, hi_y + 1):
            line = ""
            for x in range(lo_x, hi_x + 1):
                if (x, y) in self.elves:
                    line += "O" if (x, y) == (0, 0) else "#"
                else:
                    line += "o" if (x, y) == (0, 0) else "."
            logging.info(line)


# Step 1 class
class D23Step1Puzzle(D23Puzzle):
    def solve(self) -> int:
        # Iterate 10 rounds
        self.draw()
        for _ in range(10):
            self.run()

        # Reckon empty tiles = grid area - number of elves
        lo_x, lo_y, hi_x, hi_y = self.bounds()
        return (hi_x - lo_x + 1) * (hi_y - lo_y + 1) - len(self.elves)


# Step 2 class
class D23Step2Puzzle(D23Puzzle):
    def solve(self) -> int:
        # Count until the is no move
        rounds = 0
        while True:
            rounds += 1
            if not self.run():
                break
        return rounds
