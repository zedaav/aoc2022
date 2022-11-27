from abc import ABC, abstractmethod
from pathlib import Path


# Base class for puzzle solutions
class AOCPuzzle(ABC):
    def __init__(self, input_file: Path):
        # Parse input file
        self.input_file = input_file
        assert self.input_file.is_file(), f"File not found: {self.input_file}"
        with self.input_file.open() as f:
            self.input_lines = [line.strip("\r\n ") for line in f.readlines()]

    @abstractmethod
    def solve(self) -> int:  # pragma: no cover
        pass
