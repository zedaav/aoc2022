from pathlib import Path
from typing import List

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/20
"""


# Puzzle class
class D20Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.initial_numbers = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Add number
        new_number = int(trimmed_line)
        self.initial_numbers.append(new_number)

        return trimmed_line

    def mix(self, input_numbers: List[int], count: int) -> int:
        # Iterate on numbers
        total_size = len(input_numbers)
        working_copy = [(index, i) for index, i in enumerate(input_numbers)]
        for _ in range(count):
            for index, i in enumerate(input_numbers):
                # Old position
                old_index = working_copy.index((index, i))
                working_copy.remove((index, i))

                # Insert in new position
                working_copy.insert((old_index + i + total_size - 1) % (total_size - 1), (index, i))

        # Find digits after 0
        init_pos = working_copy.index((input_numbers.index(0), 0))
        result = 0
        for digit in range(1, 4):
            result += working_copy[(init_pos + digit * 1000) % total_size][1]
        return result


# Step 1 class
class D20Step1Puzzle(D20Puzzle):
    def solve(self) -> int:
        # 1 iteration on original numbers
        return self.mix(self.initial_numbers, 1)


# Step 2 class
class D20Step2Puzzle(D20Puzzle):
    def solve(self) -> int:
        # 10 iteration on multiplied numbers
        return self.mix([n * 811589153 for n in self.initial_numbers], 10)
