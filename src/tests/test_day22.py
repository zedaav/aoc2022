from aoc2022.day22 import D22Step1Puzzle, D22Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD22(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D22Step1Puzzle, "d22.sample.txt", 6032)

    def test_step1_input(self):
        self.check_solution(D22Step1Puzzle, "d22.input.txt", 11464)

    def test_step2_input(self):
        self.check_solution(D22Step2Puzzle, "d22.input.txt", 197122)
