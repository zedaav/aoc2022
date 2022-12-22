import re
from pathlib import Path

import z3

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

        # Super call
        super().__init__(input_file)
        self.vars = {}

    def add_var(self, name: str):
        if name not in self.vars:
            self.vars[name] = z3.Int(name)
        return self.vars[name]

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
            self.monkeys[m.group(1)] = (m.group(3), m.group(2), m.group(4))

        return trimmed_line

    def resolve(self, target: str) -> int:
        # Setup solver
        s = z3.Solver()
        self.add_var(target)
        for name, candidate in self.monkeys.items():
            if isinstance(candidate, int):
                if name != "humn" or target != "humn":
                    s.add(self.add_var(name) == candidate)
            else:
                op, a, b = candidate
                if name == "root" and target != "root":
                    s.add(self.add_var(a) == self.add_var(b))
                elif op == "+":
                    s.add(self.add_var(name) == self.add_var(a) + self.add_var(b))
                elif op == "-":
                    s.add(self.add_var(a) == self.add_var(name) + self.add_var(b))
                elif op == "*":
                    s.add(self.add_var(name) == self.add_var(a) * self.add_var(b))
                else:  # if op == "/":
                    s.add(self.add_var(a) == self.add_var(name) * self.add_var(b))

        # Resolve
        s.check()
        return s.model().eval(self.vars[target])


# Step 1 class
class D21Step1Puzzle(D21Puzzle):
    def solve(self) -> int:
        # Solve for root variable
        return self.resolve("root")


# Step 2 class
class D21Step2Puzzle(D21Puzzle):
    def solve(self) -> int:
        # Solve for human variable
        return self.resolve("humn")
