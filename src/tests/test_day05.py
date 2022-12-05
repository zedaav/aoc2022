from aoc2022.day05 import D05Step1Puzzle, D05Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD05(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D05Step1Puzzle, "d05.sample.txt", "CMZ")

    def test_step1_input(self):
        self.check_solution(D05Step1Puzzle, "d05.input.txt", "FRDSQRRCD")

    def test_step2_sample(self):
        self.check_solution(D05Step2Puzzle, "d05.sample.txt", "MCD")

    def test_step2_input(self):
        self.check_solution(D05Step2Puzzle, "d05.input.txt", "HRFTQVWNN")
