from aoc2022.day04 import D04Step1Puzzle, D04Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD04(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D04Step1Puzzle, "d04.sample.txt", 2)

    def test_step1_input(self):
        self.check_solution(D04Step1Puzzle, "d04.input.txt", 530)

    def test_step2_sample(self):
        self.check_solution(D04Step2Puzzle, "d04.sample.txt", 4)

    def test_step2_input(self):
        self.check_solution(D04Step2Puzzle, "d04.input.txt", 903)
