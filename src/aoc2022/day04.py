import logging
import re
from abc import abstractmethod
from pathlib import Path
from typing import Set

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/4
"""

# Pattern for section
SECTION_PATTERN = re.compile("([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)")


# Puzzle class
class D04Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.overlaps = 0

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        # Check for sections parsing
        m = SECTION_PATTERN.match(parsed_line)
        assert m is not None, f"Can't parse line {index}: {parsed_line}"
        section1 = set(range(int(m.group(1)), int(m.group(2)) + 1))
        section2 = set(range(int(m.group(3)), int(m.group(4)) + 1))
        logging.info(f"New sections on line {index}: {section1} vs {section2}")

        # Handle sections
        self.handle_sections(section1, section2)

        return parsed_line

    @abstractmethod
    def handle_sections(self, section1: Set[int], section2: Set[int]):  # pragma: no cover
        pass

    def solve(self) -> int:
        # Solution is overlaps count
        return self.overlaps


# Step 1 class
class D04Step1Puzzle(D04Puzzle):
    def handle_sections(self, section1: Set[int], section2: Set[int]):
        # Check for full section overlap
        overlap = section1 & section2
        if overlap == section1 or overlap == section2:
            logging.info("One more overlap")
            self.overlaps += 1


# Step 2 class
class D04Step2Puzzle(D04Puzzle):
    def handle_sections(self, section1: Set[int], section2: Set[int]):
        # Check for full section overlap
        overlap = section1 & section2
        if len(overlap):
            logging.info("One more overlap")
            self.overlaps += 1
