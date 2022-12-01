from aoc2022.day01 import D01Step1Puzzle, D01Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD01(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D01Step1Puzzle, "d01.sample.txt", 24000)

    def test_step1_input(self):
        self.check_solution(D01Step1Puzzle, "d01.input.txt", 69693)

    def test_step2_sample(self):
        self.check_solution(D01Step2Puzzle, "d01.sample.txt", 45000)

    def test_step2_input(self):
        self.check_solution(D01Step2Puzzle, "d01.input.txt", 200945)

    def test_malformed(self):
        try:
            self.check_solution(D01Step1Puzzle, "d01.malformed.txt", 0)
        except AssertionError as e:
            assert "Can't parse calories count" in str(e)
