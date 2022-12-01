from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/1
"""


class D01Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Prepare puzzle data
        self.calories = []
        self.next_elf_calories = 0

        # Super call
        super().__init__(input_file)

        # Last call if no new line at the end of the input
        self.handle_new_elf()

    def handle_new_elf(self):
        if self.next_elf_calories > 0:
            # New elf
            self.calories.append(self.next_elf_calories)
            self.next_elf_calories = 0

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        parsed_line = super().parse_line(index, line)

        # Something to add?
        if len(parsed_line):
            # Should be an int
            try:
                calories_count = int(parsed_line)
                self.next_elf_calories += calories_count
            except ValueError as e:
                raise AssertionError(f"Can't parse calories count ('{parsed_line}') at line {index}: {e}")
        else:
            # New elf
            self.handle_new_elf()


class D01Step1Puzzle(D01Puzzle):
    def solve(self) -> int:
        # Just max of all found calories
        return max(self.calories)


class D01Step2Puzzle(D01Puzzle):
    def solve(self) -> int:
        # Sort calories, and sum the last 3 ones
        return sum(sorted(self.calories)[-3:])
