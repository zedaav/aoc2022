import re
from pathlib import Path

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/16
"""

# Pattern for instruction line
INST_PATTERN = re.compile("Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)")
VALVES_SEP = ", "


# Puzzle class
class D16Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Init puzzle data
        self.flows = {}
        self.targets = {}

        # Super call
        super().__init__(input_file)

        # Map of positions per flow
        self.powers = {x: 1 << i for i, x in enumerate(self.flows)}

        # Permutations
        self.perms = {x: {y: 1 if y in self.targets[x] else float("+inf") for y in self.targets} for x in self.targets}
        for k in self.perms:
            for i in self.perms:
                for j in self.perms:
                    self.perms[i][j] = min(self.perms[i][j], self.perms[i][k] + self.perms[k][j])

    def parse_line(self, index: int, line: str) -> str:
        # Super call
        trimmed_line = super().parse_line(index, line)

        # Parse line and build flows/targets maps
        m = INST_PATTERN.match(trimmed_line)
        assert m is not None
        pos = m.group(1)
        flow = int(m.group(2))
        if flow != 0:
            self.flows[pos] = flow
        self.targets[pos] = set(m.group(3).split(VALVES_SEP))

        return trimmed_line

    def visit(self, pos, budget, state, value, answer):
        answer[state] = max(answer.get(state, 0), value)
        for u in self.flows:
            newbudget = budget - self.perms[pos][u] - 1
            if self.powers[u] & state or newbudget < 0:
                continue
            self.visit(u, newbudget, state | self.powers[u], value + newbudget * self.flows[u], answer)
        return answer


# Step 1 class
class D16Step1Puzzle(D16Puzzle):
    def solve(self) -> int:
        # Browse once
        return max(self.visit("AA", 30, 0, 0, {}).values())


# Step 2 class
class D16Step2Puzzle(D16Puzzle):
    def solve(self) -> int:
        # Browse and sum
        visited2 = self.visit("AA", 26, 0, 0, {})
        return max(v1 + v2 for k1, v1 in visited2.items() for k2, v2 in visited2.items() if not k1 & k2)
