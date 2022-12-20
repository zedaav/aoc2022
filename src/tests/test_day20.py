from aoc2022.day20 import D20Step1Puzzle, D20Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD20(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D20Step1Puzzle, "d20.sample.txt", 3)

    def test_step1_input(self):
        self.check_solution(D20Step1Puzzle, "d20.input.txt", 4066)

    def test_step2_sample(self):
        self.check_solution(D20Step2Puzzle, "d20.sample.txt", 1623178306)

    def test_step2_input(self):
        self.check_solution(D20Step2Puzzle, "d20.input.txt", 6704537992933)
