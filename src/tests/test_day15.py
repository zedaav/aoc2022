from aoc2022.day15 import D15Step1Puzzle, D15Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD15(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D15Step1Puzzle, "d15.sample.txt", 26, solve_arg=10)

    def test_step1_input(self):
        self.check_solution(D15Step1Puzzle, "d15.input.txt", 4873353, solve_arg=2_000_000)

    def test_step2_sample(self):
        self.check_solution(D15Step2Puzzle, "d15.sample.txt", 56000011, solve_arg=20)

    def test_step2_input(self):
        self.check_solution(D15Step2Puzzle, "d15.input.txt", 11600823139120, solve_arg=4_000_000)
