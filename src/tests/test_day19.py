from aoc2022.day19 import D19Step1Puzzle, D19Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD19(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D19Step1Puzzle, "d19.sample.txt", 33)

    def test_step1_input(self):
        self.check_solution(D19Step1Puzzle, "d19.input.txt", 1480)

    def test_step2_sample(self):
        self.check_solution(D19Step2Puzzle, "d19.sample.txt", 3472)

    def test_step2_input(self):
        self.check_solution(D19Step2Puzzle, "d19.input.txt", 3168)
