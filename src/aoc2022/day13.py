import functools
import json
import logging
from pathlib import Path
from typing import Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/13
"""


# Compare function
def compare(left: Union[str, list], right: Union[str, list]) -> bool:
    # Both are integers?
    if isinstance(left, int) and isinstance(right, int):
        # Check order
        if left < right:
            return -1
        if left > right:
            return 1
        return 0
    else:
        # List compare
        left_list = list(left) if isinstance(left, list) else [left]
        right_list = list(right) if isinstance(right, list) else [right]

        # Iterate
        while True:
            # Check if one of the list ran out of items
            left_len = len(left_list)
            right_len = len(right_list)
            if not left_len and right_len:
                return -1
            if not right_len and left_len:
                return 1

            # Compare items (if there are still ones)
            if left_len and right_len:
                r = compare(left_list.pop(0), right_list.pop(0))
                if r != 0:
                    return r
            else:
                return 0


# Puzzle class
class D13Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.next_left = None
        self.next_right = None
        self.pairs = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Something to parse?
        if len(trimmed_line):
            candidate_list = json.loads(trimmed_line)
            if self.next_left is None:
                self.next_left = candidate_list
            else:
                self.next_right = candidate_list
        else:
            # Remember pair of list
            self.pairs.append((self.next_left, self.next_right))
            logging.info(f"New pair #{len(self.pairs)}: {self.next_left} vs {self.next_right}")
            self.next_left = None
            self.next_right = None

        return trimmed_line


# Step 1 class
class D13Step1Puzzle(D13Puzzle):
    def solve(self) -> int:
        # Compare all pairs
        correct_count = 0
        for index, (left, right) in enumerate(self.pairs, start=1):
            # Recursive comparison
            if compare(left, right) < 0:
                correct_count += index
        return correct_count


# Step 2 class
class D13Step2Puzzle(D13Puzzle):
    KEY1 = [[2]]
    KEY2 = [[6]]

    def solve(self) -> int:
        # Sort the whole list + insert other items
        whole_list = [D13Step2Puzzle.KEY1, D13Step2Puzzle.KEY2]
        for left, right in self.pairs:
            whole_list.extend([left, right])
        sorted_list = sorted(whole_list, key=functools.cmp_to_key(compare))
        return (sorted_list.index(D13Step2Puzzle.KEY1) + 1) * (sorted_list.index(D13Step2Puzzle.KEY2) + 1)
