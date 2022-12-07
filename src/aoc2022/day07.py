import logging
import re
from pathlib import Path
from typing import Union

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/7
"""

# Prefixes & patterns
PREFIX_CD = "$ cd "
PREFIX_LS = "$ ls"
PREFIX_DIR = "dir "
FILE_PATTERN = re.compile("([0-9]+) +.*")
ROOT_PATH = "/"


# Puzzle class
class D07Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.cwd = Path(ROOT_PATH)
        self.sizes = {}
        self.handle_new_dir()

        # Super call
        super().__init__(input_file)

    def handle_new_dir(self):
        # Already known?
        if self.cwd not in self.sizes:
            logging.info(f"Handle new directory: {self.cwd}")
            self.sizes[self.cwd] = 0

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        parsed_line = super().parse_line(index, line)

        # Checks commands
        if parsed_line.startswith(PREFIX_CD):
            # Change directory
            new_dir = parsed_line[len(PREFIX_CD) :]
            if new_dir == ROOT_PATH:
                self.cwd = Path(ROOT_PATH)
            else:
                self.cwd = (self.cwd / new_dir).resolve()
            self.handle_new_dir()
        elif parsed_line.startswith(PREFIX_LS):
            # Just the ls command; toggle size grabbing only if not done yet for this path
            logging.info(f"Start grabbing sizes for {self.cwd}")
        elif parsed_line.startswith(PREFIX_DIR):
            # New dir... but actually we don't care
            pass
        else:
            # Last case is size reckoning
            m = FILE_PATTERN.match(parsed_line)
            assert m is not None
            new_size = int(m.group(1))

            # Add this size to cwd and all parents
            path_to_add = self.cwd
            while True:
                self.sizes[path_to_add] += new_size
                logging.info(f" >> Add {new_size} to {path_to_add} -- new size is {self.sizes[path_to_add]}")
                if path_to_add == Path(ROOT_PATH):
                    break
                else:
                    path_to_add = path_to_add.parent

        return parsed_line


# Step 1 class
class D07Step1Puzzle(D07Puzzle):
    def solve(self) -> Union[int, str]:
        # Solution is sum of sizes < 100000
        return sum(filter(lambda s: s <= 100000, self.sizes.values()))


# Step 2 class
class D07Step2Puzzle(D07Puzzle):
    def solve(self) -> Union[int, str]:
        # Currently used space
        current_used = self.sizes[Path(ROOT_PATH)]
        current_free = 70000000 - current_used
        need_to_free = 30000000 - current_free

        # Solution is sum of sizes < 100000
        return min(filter(lambda s: s >= need_to_free, self.sizes.values()))
