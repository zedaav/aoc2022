from aoc2022.day24 import D24Step1Puzzle, D24Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD24(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D24Step1Puzzle, "d24.sample.txt", 18)

    def test_step1_input(self):
        self.check_solution(D24Step1Puzzle, "d24.input.txt", 286)

    def test_step2_sample(self):
        self.check_solution(D24Step2Puzzle, "d24.sample.txt", 54)

    def test_step2_input(self):
        self.check_solution(D24Step2Puzzle, "d24.input.txt", 820)
