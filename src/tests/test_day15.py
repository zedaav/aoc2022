from aoc2022.day15 import D15Step1Puzzle, D15Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD15(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D15Step1Puzzle, "d15.sample.txt", 0)

    def test_step1_input(self):
        self.check_solution(D15Step1Puzzle, "d15.input.txt", 0)

    def test_step2_sample(self):
        self.check_solution(D15Step2Puzzle, "d15.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D15Step2Puzzle, "d15.input.txt", 0)
