import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/8
"""


# Tree class
@dataclass
class Tree:
    value: int
    left_ones: List[int]
    right_ones: List[int]
    top_ones: List[int]
    bottom_ones: List[int]

    def __repr__(self) -> str:
        return f"Tree(v: {self.value}, left:{self.left_ones}, right:{self.right_ones}, top:{self.top_ones}, bottom:{self.bottom_ones})"


# Puzzle class
class D08Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.trees = {}
        self.int_lines = []

        # Super call
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)
        logging.info(f"handling new line {index}")

        # Browse each tree in the line
        int_line = [int(c) for c in trimmed_line]
        y = index
        for x, tree_value in enumerate(int_line):
            # Persist in map:
            # * tree coordinates (x,y) as keys
            # * tree items (tree value, list of all neighbor trees) as values

            # 1. trees on the left
            left_ones = int_line[0:x]

            # 2. trees on the right
            right_ones = int_line[x + 1 :]

            # 3. trees on the top
            top_ones = [ln[x] for ln in self.int_lines]

            # 4. compute trees on the bottom for all already processed trees on the same column
            for (_x, _y), t in filter(lambda t: t[0][0] == x, self.trees.items()):
                t.bottom_ones.append(tree_value)

            # Remember tree
            new_t = Tree(tree_value, left_ones, right_ones, top_ones, [])
            self.trees[(x, y)] = new_t

        # Remember line of trees
        self.int_lines.append(int_line)

        return trimmed_line


# Step 1 class
class D08Step1Puzzle(D08Puzzle):
    def solve(self) -> Union[int, str]:
        # Count all trees greater than at least one of its neighbors lists
        count = 0
        for (x, y), t in self.trees.items():
            logging.info(f"Check tree at ({x}, {y}): {t}")
            for n in [t.left_ones, t.right_ones, t.top_ones, t.bottom_ones]:
                if not len(n) or (t.value > max(n)):
                    count += 1
                    break

        return count


# Step 2 class
class D08Step2Puzzle(D08Puzzle):
    pass
