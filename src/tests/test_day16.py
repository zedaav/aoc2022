from aoc2022.day16 import D16Step1Puzzle, D16Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD16(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D16Step1Puzzle, "d16.sample.txt", 0)

    def test_step1_input(self):
        self.check_solution(D16Step1Puzzle, "d16.input.txt", 0)

    def test_step2_sample(self):
        self.check_solution(D16Step2Puzzle, "d16.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D16Step2Puzzle, "d16.input.txt", 0)
