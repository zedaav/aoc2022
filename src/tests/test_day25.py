from aoc2022.day25 import D25Step1Puzzle
from tests.base import AOCPuzzleTester


class TestD25(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D25Step1Puzzle, "d25.sample.txt", "2=-1=0")

    def test_step1_input(self):
        self.check_solution(D25Step1Puzzle, "d25.input.txt", "20==1==12=0111=2--20")
