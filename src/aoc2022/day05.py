import logging
import re
from abc import abstractmethod
from pathlib import Path
from typing import Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/5
"""

# Crate delimiter
CRATE_DELIMITER = "["

# Instruction pattern
INSTRUCTION_PATTERN = re.compile("move ([0-9]+) from ([0-9]+) to ([0-9]+)")


# Puzzle class
class D05Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.stacks = {}

        # Super call
        super().__init__(input_file)

        # Dump stacks after parsing
        logging.info(f"Final stacks position: {self.stacks}")

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        # Check for input part
        if len(parsed_line):
            if CRATE_DELIMITER in parsed_line:
                # Crate line
                self.parse_crates(index, line)  # use "no trim" version
            else:
                # Try with instruction pattern
                m = INSTRUCTION_PATTERN.match(parsed_line)
                if m is not None:
                    # Instruction found
                    from_pos, to_pos = (int(m.group(2)), int(m.group(3)))
                    assert from_pos in self.stacks
                    assert to_pos in self.stacks
                    self.handle_instruction(int(m.group(1)), from_pos, to_pos)
                else:
                    # Just the line of stacks; dump them
                    logging.info(f"At line {index}, parsed stacks: {self.stacks}")

        return parsed_line

    def parse_crates(self, index: int, line: str):
        # Loop on crates
        last_pos = 0
        while True:
            # Find next crate on this line
            delim_pos = line.find(CRATE_DELIMITER, last_pos)
            if delim_pos >= 0:
                # Validate positions
                assert delim_pos % 4 == 0
                crate_pos = int(delim_pos / 4) + 1
                last_pos = delim_pos + 1

                # Add to stack
                current_stack = "" if crate_pos not in self.stacks else self.stacks[crate_pos]
                self.stacks[crate_pos] = line[delim_pos + 1] + current_stack
            else:
                break

    @abstractmethod
    def handle_instruction(self, size: int, from_pos: int, to_pos: int):  # pragma: no cover
        pass

    def solve(self) -> Union[int, str]:
        # Top level crates
        out = ""
        for pos in range(1, len(self.stacks) + 1):
            out += self.stacks[pos][-1:]
        return out


# Step 1 class
class D05Step1Puzzle(D05Puzzle):
    def handle_instruction(self, size: int, from_pos: int, to_pos: int):
        # Do the move (crates in reverse order)
        source_stack = self.stacks[from_pos]
        self.stacks[from_pos] = source_stack[:-size]
        self.stacks[to_pos] = self.stacks[to_pos] + source_stack[-size:][::-1]


# Step 2 class
class D05Step2Puzzle(D05Puzzle):
    def handle_instruction(self, size: int, from_pos: int, to_pos: int):
        # Do the move (crates in same order)
        source_stack = self.stacks[from_pos]
        self.stacks[from_pos] = source_stack[:-size]
        self.stacks[to_pos] = self.stacks[to_pos] + source_stack[-size:]
