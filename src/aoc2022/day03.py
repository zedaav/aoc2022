import logging
from functools import lru_cache
from pathlib import Path
from typing import Tuple, Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/3
"""

# Common codes
BIG_A_CODE = ord("A")
SMALL_A_CODE = ord("a")


# Reckon item priority
@lru_cache
def priority(item: str) -> int:
    # Reckon priority from common element
    code = ord(item)
    if code >= SMALL_A_CODE:
        return code - SMALL_A_CODE + 1
    return code - BIG_A_CODE + 27


# Find common element
@lru_cache
def common_element(candidates: Tuple[str]) -> str:
    # Iterate to find common element
    remaining_set = set(candidates[0])
    for other_set in map(set, candidates[1:]):
        remaining_set = remaining_set & other_set
    assert len(remaining_set) == 1, f"Can't find a common element from {candidates} / {remaining_set}"
    return remaining_set.pop()


# Puzzle class
class D03Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Prepare puzzle data
        self.common_items = []

        # Super call
        super().__init__(input_file)

    def solve(self) -> Union[int, str]:
        # Sum the priorities
        return sum(priority(c) for c in self.common_items)


# Step 1 class
class D03Step1Puzzle(D03Puzzle):
    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        # Parse content string
        content_len = len(parsed_line)
        assert content_len % 2 == 0, f"Error while parsing bag content at line {index}: length is not even ({parsed_line})"
        half_len = int(content_len / 2)

        # Find common element
        common = common_element((parsed_line[:half_len], parsed_line[half_len:]))

        # Ok!
        logging.info(f"New bag at line {index}; common element: {common}; priority: {priority(common)}")
        self.common_items.append(common)

        return parsed_line


# Step 2 class
class D03Step2Puzzle(D03Puzzle):
    def __init__(self, input_file: Path):
        # Prepare puzzle data
        self.group_of_3 = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        # Add to group
        self.group_of_3.append(parsed_line)
        if len(self.group_of_3) == 3:
            # Time to look for common item
            common = common_element(tuple(self.group_of_3))
            logging.info(f"New common item at line {index}: {common}; priority: {priority(common)}")
            self.common_items.append(common)

            # Clear group
            self.group_of_3.clear()

        return parsed_line
