from aoc2022.day23 import D23Step1Puzzle, D23Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD23(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D23Step1Puzzle, "d23.sample.txt", 110)

    def test_step1_input(self):
        self.check_solution(D23Step1Puzzle, "d23.input.txt", 3762)

    def test_step2_sample(self):
        self.check_solution(D23Step2Puzzle, "d23.sample.txt", 20)

    def test_step2_input(self):
        self.check_solution(D23Step2Puzzle, "d23.input.txt", 997)
