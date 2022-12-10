from aoc2022.day11 import D11Step1Puzzle, D11Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD11(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D11Step1Puzzle, "d11.sample.txt", 0)

    def test_step1_input(self):
        self.check_solution(D11Step1Puzzle, "d11.input.txt", 0)

    def test_step2_sample(self):
        self.check_solution(D11Step2Puzzle, "d11.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D11Step2Puzzle, "d11.input.txt", 0)
