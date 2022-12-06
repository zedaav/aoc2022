from aoc2022.day07 import D07Step1Puzzle, D07Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD07(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D07Step1Puzzle, "d07.sample.txt", 0)

    def test_step1_input(self):
        self.check_solution(D07Step1Puzzle, "d07.input.txt", 0)

    def test_step2_sample(self):
        self.check_solution(D07Step2Puzzle, "d07.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D07Step2Puzzle, "d07.input.txt", 0)
