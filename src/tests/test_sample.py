from aoc2022.sample import AOCSamplePuzzle
from tests.base import AOCPuzzleTester


class TestSample(AOCPuzzleTester):
    def test_sample(self):
        self.check_solution(AOCSamplePuzzle, "sample.txt", 2)
