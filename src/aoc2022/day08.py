import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import numpy

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


# Puzzle class
class D08Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.trees = {}
        self.int_lines = []

        # Super call
        super().__init__(input_file)

        # Build an array with everything
        tree_array = numpy.array(self.int_lines)
        logging.info(f"Built array:\n{tree_array}")

        # Browse all trees
        for y in range(len(self.int_lines)):
            for x in range(len(self.int_lines[0])):
                self.trees[(x, y)] = Tree(
                    tree_array[y][x],  # Tree value (= height)
                    tree_array[y][0:x][::-1],  # Trees on the left (from closest to farest)
                    tree_array[y][x + 1 :],  # Trees on the right
                    tree_array[:, x][0:y][::-1],  # Trees on the top (from closest to farest)
                    tree_array[:, x][y + 1 :],  # Trees on the bottom
                )

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # New line
        self.int_lines.append([int(c) for c in trimmed_line])

        return trimmed_line


# Step 1 class
class D08Step1Puzzle(D08Puzzle):
    def solve(self) -> Union[int, str]:
        # Count all trees greater than at least one of its neighbors lists
        count = 0
        for (_x, _y), t in self.trees.items():
            for n in [t.left_ones, t.right_ones, t.top_ones, t.bottom_ones]:
                if not len(n) or (t.value > max(n)):
                    count += 1
                    break

        return count


# Step 2 class
class D08Step2Puzzle(D08Puzzle):
    def solve(self) -> Union[int, str]:
        # Browse all trees not on the borders
        top_scenic_score = 0
        for y in range(1, len(self.int_lines) - 1):
            for x in range(1, len(self.int_lines[0]) - 1):
                # Get distance to closest neighbor tree at least as tall as current tree, in all directions
                tree = self.trees[(x, y)]
                scenic_score = 1
                for trees in [tree.left_ones, tree.right_ones, tree.top_ones, tree.bottom_ones]:
                    # Default distance is distance to the border
                    max_dist = len(trees)
                    for dist, neighbor in enumerate(trees, 1):
                        if neighbor >= tree.value:
                            # Closer distance: a neighbor tree is at least as tall as current tree
                            max_dist = dist
                            break
                    scenic_score *= max_dist

                # Better score?
                if scenic_score > top_scenic_score:
                    top_scenic_score = scenic_score

        return top_scenic_score
