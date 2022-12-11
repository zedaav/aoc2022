from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/6
"""


# Puzzle class
class D06Puzzle(AOCPuzzle):
    # Default packet len
    # Not set in __init__ because it will be initialized by sub-classes
    packet_len = 0

    def __init__(self, input_file: Path):
        # Init puzzle data
        self.packet_pos = 0

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        # Iterate on character sets
        for pos in range(self.packet_len, len(parsed_line)):  # pragma: no branch
            # Build candidate
            candidate = parsed_line[pos - self.packet_len : pos]

            # Check for repetitions in candidate
            if len(set(candidate)) == self.packet_len:
                self.packet_pos = pos
                break

        return parsed_line

    def solve(self) -> int:
        # Solution is first packet position
        return self.packet_pos


# Step 1 class
class D06Step1Puzzle(D06Puzzle):
    def __init__(self, input_file: Path):
        # Set packet length
        self.packet_len = 4
        super().__init__(input_file)


# Step 2 class
class D06Step2Puzzle(D06Puzzle):
    def __init__(self, input_file: Path):
        # Set packet length
        self.packet_len = 14
        super().__init__(input_file)
