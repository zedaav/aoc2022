import logging
import re
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, List, Tuple

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/11
"""


# Monkey class
@dataclass
class Monkey:
    items: List[int]
    operation: Callable
    divisor: int
    target_true: int
    target_false: int
    with_division: bool
    process_count: int = 0

    def process(self) -> Tuple[int, int]:
        """
        Process next monkey item, and get ready to throw it to another monkey
        """

        # Something to do?
        if not len(self.items):
            return None

        # Process next item
        item = self.items.pop(0)
        item = self.operation(item)
        if self.with_division:
            item = int(item / 3)
        divisible = (item % self.divisor) == 0  # NOQA: S001
        target = self.target_true if divisible else self.target_false

        # One more operation
        self.process_count += 1

        return (item, target)


# Patterns
class PatternID(Enum):
    START = 0
    ITEMS = 1
    OPERATION = 2
    TEST = 3
    IF_TRUE = 4
    IF_FALSE = 5
    SEPARATOR = 6


ALL_PATTERNS = {
    PatternID.START: re.compile("Monkey ([0-9]+):"),
    PatternID.ITEMS: re.compile("Starting items: ([0-9, ]+)"),
    PatternID.OPERATION: re.compile("Operation: new = old ([+\\*]) ((old)|[0-9]+)"),
    PatternID.TEST: re.compile("Test: divisible by ([0-9]+)"),
    PatternID.IF_TRUE: re.compile("If true: throw to monkey ([0-9]+)"),
    PatternID.IF_FALSE: re.compile("If false: throw to monkey ([0-9]+)"),
    PatternID.SEPARATOR: None,
}
ITEMS_SEPARATOR = ", "


# Puzzle class
class D11Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.next_monkey_id = 0
        self.next_monkey_items = []
        self.next_monkey_operation = None
        self.next_monkey_divisor = 0
        self.next_monkey_target_true = 0
        self.next_monkey_target_false = 0
        self.monkeys = {}

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Parse lines
        pid = PatternID((index - 1) % len(ALL_PATTERNS))
        if pid != PatternID.SEPARATOR:
            # Not a separator line: parse according to expected pattern
            m = ALL_PATTERNS[pid].match(trimmed_line)
            assert m is not None

            # Operate according to current line pattern
            if pid == PatternID.START:
                self.next_monkey_id = int(m.group(1))
            elif pid == PatternID.ITEMS:
                self.next_monkey_items = [int(i) for i in m.group(1).split(ITEMS_SEPARATOR)]
            elif pid == PatternID.OPERATION:
                if m.group(1) == "+":
                    self.next_monkey_operation = lambda old: old + int(m.group(2))
                else:
                    if m.group(2) == "old":
                        self.next_monkey_operation = lambda old: old * old
                    else:
                        self.next_monkey_operation = lambda old: old * int(m.group(2))
            elif pid == PatternID.TEST:
                self.next_monkey_divisor = int(m.group(1))
            elif pid == PatternID.IF_TRUE:
                self.next_monkey_target_true = int(m.group(1))
            else:
                self.next_monkey_target_false = int(m.group(1))
                self.monkeys[self.next_monkey_id] = Monkey(
                    self.next_monkey_items,
                    self.next_monkey_operation,
                    self.next_monkey_divisor,
                    self.next_monkey_target_true,
                    self.next_monkey_target_false,
                    self.with_division,
                )

        return trimmed_line

    @property
    @abstractmethod
    def with_division(self) -> bool:  # pragma: no cover
        pass

    def process(self, rounds: int):
        # Process cycles
        for r in range(rounds):
            # Process monkeys
            for mid in range(len(self.monkeys)):
                monkey = self.monkeys[mid]
                while True:
                    candidate = monkey.process()
                    if candidate is None:
                        break
                    item, target = candidate
                    self.monkeys[target].items.append(item)

            logging.info(f"== After round {r+1} ==")
            for mid, monkey in self.monkeys.items():
                logging.info(f"Monkey {mid} inspected items {monkey.process_count} times.")

        # Result is product of two most active monkeys
        counts = sorted(m.process_count for m in self.monkeys.values())
        return counts[-1] * counts[-2]


# Step 1 class
class D11Step1Puzzle(D11Puzzle):
    @property
    def with_division(self) -> bool:
        return True

    def solve(self) -> int:
        # Result is product of two most active monkeys after 20 rounds
        return self.process(20)


# Step 2 class
class D11Step2Puzzle(D11Puzzle):
    @property
    def with_division(self) -> bool:
        return False

    def solve(self) -> int:
        # Result is product of two most active monkeys after 10000 rounds
        return self.process(10000)
