from aoc2022.puzzle import AOCPuzzle


class AOCSamplePuzzle(AOCPuzzle):
    def solve(self) -> int:
        # Sample: just return input size
        return len(self.input_lines)
