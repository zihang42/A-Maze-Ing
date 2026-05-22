from .utils import AlgorithmSolve


class AstartSolve(AlgorithmSolve):
    def solve(self) -> list[tuple[int, int]]:
        return [self.entry]
