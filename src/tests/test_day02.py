from aoc2022.day02 import D02Step1Puzzle, D02Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD02(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D02Step1Puzzle, "d02.sample.txt", 15)

    def test_step1_input(self):
        self.check_solution(D02Step1Puzzle, "d02.input.txt", 9759)

    def test_step2_sample(self):
        self.check_solution(D02Step2Puzzle, "d02.sample.txt", 12)

    def test_step2_input(self):
        self.check_solution(D02Step2Puzzle, "d02.input.txt", 12429)
