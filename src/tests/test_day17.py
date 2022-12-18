from aoc2022.day17 import D17Step1Puzzle, D17Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD17(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D17Step1Puzzle, "d17.sample.txt", 3068)

    def test_step1_input(self):
        self.check_solution(D17Step1Puzzle, "d17.input.txt", 3059)

    def test_step2_sample(self):
        self.check_solution(D17Step2Puzzle, "d17.sample.txt", 1514285714288)

    def test_step2_input(self):
        self.check_solution(D17Step2Puzzle, "d17.input.txt", 1500874635587)
