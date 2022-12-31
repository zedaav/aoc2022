import logging

from aoc2022.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2022/day/25
"""

# SNAFU digit to decimal digit
SNAFU_TO_DEC = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}

# Decimal digit to SNAFU digit
DEC_TO_SNAFU = {3: "=", 4: "-", 0: "0", 1: "1", 2: "2", 5: "0"}


# Puzzle class
class D25Step1Puzzle(AOCPuzzle):
    def snafu_to_dec(self, snafu: str) -> int:
        # Iterate in base 5
        result = 0
        for pos, digit in enumerate(reversed(snafu)):
            result += 5**pos * SNAFU_TO_DEC[digit]
        return result

    def dec_to_snafu(self, dec: int) -> str:
        # Iterate on divisions/modulo by 5
        digits = []
        r = 0
        while dec > 0:
            x = dec % 5 + r
            digits.insert(0, DEC_TO_SNAFU[x])
            r = 1 if x > 2 else 0
            dec //= 5
        return "".join(digits)

    def solve(self) -> str:
        # Convert all snafu numbers
        dec_result = sum(self.snafu_to_dec(snafu) for snafu in self.input_lines)
        logging.info(f"decimal result: {dec_result}")
        return self.dec_to_snafu(dec_result)
