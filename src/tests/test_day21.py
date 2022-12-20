from aoc2022.day21 import D21Step1Puzzle, D21Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD21(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D21Step1Puzzle, "d21.sample.txt", 0)

    def test_step1_input(self):
        self.check_solution(D21Step1Puzzle, "d21.input.txt", 0)

    def test_step2_sample(self):
        self.check_solution(D21Step2Puzzle, "d21.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D21Step2Puzzle, "d21.input.txt", 0)
