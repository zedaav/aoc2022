from aoc2022.day18 import D18Step1Puzzle, D18Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD18(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D18Step1Puzzle, "d18.sample.txt", 64)

    def test_step1_input(self):
        self.check_solution(D18Step1Puzzle, "d18.input.txt", 4474)

    def test_step2_sample(self):
        self.check_solution(D18Step2Puzzle, "d18.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D18Step2Puzzle, "d18.input.txt", 0)
