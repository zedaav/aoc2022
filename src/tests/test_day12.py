from aoc2022.day12 import D12Step1Puzzle, D12Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD12(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D12Step1Puzzle, "d12.sample.txt", 31)

    def test_step1_input(self):
        self.check_solution(D12Step1Puzzle, "d12.input.txt", 468)

    def test_step2_sample(self):
        self.check_solution(D12Step2Puzzle, "d12.sample.txt", 29)

    def test_step2_input(self):
        self.check_solution(D12Step2Puzzle, "d12.input.txt", 459)
