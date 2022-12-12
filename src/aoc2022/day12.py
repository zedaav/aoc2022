import heapq
import logging
from pathlib import Path
from typing import Dict, Set, Tuple

import numpy

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/12
"""


# Puzzle class
class D12Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.int_lines = []
        self.start = None
        self.end = None
        self.path_candidates = {}

        # Super call
        super().__init__(input_file)

        # Build the whole map
        self.heights_map = numpy.array(self.int_lines)
        logging.info(f"Built array:\n{self.heights_map}")
        self.map_width = len(self.int_lines[0])
        self.map_height = len(self.int_lines)

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Handle start and end positions
        parsable_line = str(trimmed_line)
        if self.start is None:
            start_pos = parsable_line.find("S")
            if start_pos != -1:
                self.start = (start_pos, index - 1)
                parsable_line = parsable_line.replace("S", "a")
        if self.end is None:
            end_pos = parsable_line.find("E")
            if end_pos != -1:
                self.end = (end_pos, index - 1)
                parsable_line = parsable_line.replace("E", "z")

        # Add line
        self.int_lines.append([ord(c) - ord("a") for c in parsable_line])

        return trimmed_line

    def get_candidates(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        # Already found?
        if pos not in self.path_candidates:
            # Check candidates
            candidates = set()
            x, y = pos
            for x_off, y_off in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                n_x, n_y = (x + x_off, y + y_off)
                if (n_x >= 0) and (n_x < self.map_width) and (n_y >= 0) and (n_y < self.map_height):
                    cur_height = self.heights_map[y][x]
                    candidate_height = self.heights_map[n_y][n_x]
                    if candidate_height - cur_height >= -1:
                        # Valid candidate
                        candidates.add((n_x, n_y))

            self.path_candidates[pos] = candidates
        return set(self.path_candidates[pos])

    def all_paths(self) -> Dict[Tuple[int, int], int]:
        q = [(0, self.end)]
        path_costs = {self.end: 0}
        while q:
            cost, point = heapq.heappop(q)
            for candidate in self.get_candidates(point):
                # Not known path, or shorter path found
                if (candidate not in path_costs) or ((cost + 1) < path_costs[candidate]):
                    path_costs[candidate] = cost + 1
                    heapq.heappush(q, (cost + 1, candidate))
        return path_costs


# Step 1 class
class D12Step1Puzzle(D12Puzzle):
    def solve(self) -> int:
        # Solution is cost for start point
        return self.all_paths()[self.start]


# Step 2 class
class D12Step2Puzzle(D12Puzzle):
    def solve(self) -> int:
        # Solution is minimum cost for all 0-height points
        return min(c for (_x, _y), c in filter(lambda t: self.heights_map[t[0][1]][t[0][0]] == 0, self.all_paths().items()))
