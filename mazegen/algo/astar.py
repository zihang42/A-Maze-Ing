from .utils import AlgorithmSolve


class AstarSolve(AlgorithmSolve):
    def solve(self) -> list[tuple[int, int]]:
        return [self.entry]
