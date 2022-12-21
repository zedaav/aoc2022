import re
from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/21
"""

# Patterns
PATTERN_NUMBER = re.compile("([a-z]+): ([0-9]+)")
PATTERN_OPERATION = re.compile("([a-z]+): ([a-z]+) ([\\+-/\\*]) ([a-z]+)")


# Puzzle class
class D21Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.monkeys = {}
        self.operations = {
            "+": lambda a, b: self.resolve(a) + self.resolve(b),
            "-": lambda a, b: self.resolve(a) - self.resolve(b),
            "*": lambda a, b: self.resolve(a) * self.resolve(b),
            "/": lambda a, b: self.resolve(a) // self.resolve(b),
        }

        # Super call
        super().__init__(input_file)

    def resolve(self, name: str):
        # Return monkey value if already known
        v = self.monkeys[name]
        if not isinstance(v, int):
            # Otherwise, perform operation (recursively)
            op, a, b = v
            self.monkeys[name] = op(a, b)

        return self.monkeys[name]

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Number?
        m = PATTERN_NUMBER.match(trimmed_line)
        if m is not None:
            # Yes: remember it
            self.monkeys[m.group(1)] = int(m.group(2))
        else:
            # No: parse operation
            m = PATTERN_OPERATION.match(trimmed_line)
            assert m is not None
            self.monkeys[m.group(1)] = (self.operations[m.group(3)], m.group(2), m.group(4))

        return trimmed_line


# Step 1 class
class D21Step1Puzzle(D21Puzzle):
    def solve(self) -> int:
        # Solution is root monkey value
        return self.resolve("root")


# Step 2 class
class D21Step2Puzzle(D21Puzzle):
    pass
