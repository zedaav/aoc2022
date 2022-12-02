import logging
import re
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Tuple

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/2
"""


# Enum for Rock/Paper/Scissor game values
class RPSValue(Enum):
    A = 1  # Rock
    B = 2  # Paper
    C = 3  # Scissor

    @classmethod
    def from_name(cls, name: str) -> Enum:
        return cls.__dict__[name]


# Enum for Rock/Paper/Scissor game results
class RPSResult(Enum):
    LOST = 0
    DRAW = 3
    WON = 6


# Instructions guide pattern
GUIDE_PATTERN = re.compile("([ABC]) +([XYZ])")


# Instruction class
class Instruction(ABC):
    def __init__(self, part1: str, part2: str) -> None:
        # Build values and result from provided instructions
        self.elf_value = RPSValue.from_name(part1)
        self.my_value, self.result = self.parse_instructions(part1, part2)

    @abstractmethod
    def parse_instructions(self, part1: str, part2: str) -> Tuple[RPSValue, RPSResult]:  # pragma: no cover
        pass

    @property
    def score(self) -> int:
        # Get score from played value + result
        return self.my_value.value + self.result.value


# Puzzle class
class D02Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Prepare puzzle data
        self.scores = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Get parsed line
        parsed_line = super().parse_line(index, line)

        # Parse line
        m = GUIDE_PATTERN.match(parsed_line)
        assert m is not None, f"Can't parse line #{index}: {parsed_line}"

        # Build instruction from parsed items
        i = self.instruction_class(m.group(1), m.group(2))
        logging.info(f"New instruction on line {index}: elf played {i.elf_value} ; I played {i.my_value} ; result: {i.result} ; score: {i.score}")

        # Append score
        self.scores.append(i.score)

        return parsed_line

    @property
    @abstractmethod
    def instruction_class(self) -> Instruction:  # pragma: no cover
        pass

    def solve(self) -> int:
        # Puzzle solution is always the results sum
        return sum(self.scores)


# Class for step 1
class D02Step1Puzzle(D02Puzzle):
    # My own instructions class
    class Step1Instruction(Instruction):
        VALUE_MAP = {"X": RPSValue.A, "Y": RPSValue.B, "Z": RPSValue.C}
        RESULT_MAP = {
            RPSValue.A: {RPSValue.B: RPSResult.WON, RPSValue.C: RPSResult.LOST},
            RPSValue.B: {RPSValue.C: RPSResult.WON, RPSValue.A: RPSResult.LOST},
            RPSValue.C: {RPSValue.A: RPSResult.WON, RPSValue.B: RPSResult.LOST},
        }

        def parse_instructions(self, part1: str, part2: str) -> Tuple[RPSValue, RPSResult]:
            # In step 1, part2 is equivalent to part1
            my_value = self.VALUE_MAP[part2]

            # Reckon result
            if self.elf_value == my_value:
                result = RPSResult.DRAW
            else:
                result = self.RESULT_MAP[self.elf_value][my_value]

            return (my_value, result)

    @property
    def instruction_class(self) -> Instruction:
        return D02Step1Puzzle.Step1Instruction


# Class for step 2
class D02Step2Puzzle(D02Puzzle):
    # My own instructions class
    class Step2Instruction(Instruction):
        VALUE_MAP = {"X": RPSResult.LOST, "Y": RPSResult.DRAW, "Z": RPSResult.WON}
        RESULT_MAP = {
            RPSResult.WON: {RPSValue.A: RPSValue.B, RPSValue.B: RPSValue.C, RPSValue.C: RPSValue.A},
            RPSResult.LOST: {RPSValue.A: RPSValue.C, RPSValue.B: RPSValue.A, RPSValue.C: RPSValue.B},
        }

        def parse_instructions(self, part1: str, part2: str) -> Tuple[RPSValue, RPSResult]:
            # In step 2, part2 is the result!
            result = self.VALUE_MAP[part2]

            # Reckon my value
            if result == RPSResult.DRAW:
                my_value = self.elf_value
            else:
                my_value = self.RESULT_MAP[result][self.elf_value]

            return (my_value, result)

    @property
    def instruction_class(self) -> Instruction:
        return D02Step2Puzzle.Step2Instruction
